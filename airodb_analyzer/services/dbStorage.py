import pymongo
import sys
from pymongo import MongoClient
from airodb_analyzer.models.accessPoint import AccessPoint
from airodb_analyzer.models.macAddress import MACAddress

class DBStorage():
    def __init__(self, mongoClient=None):
      if (mongoClient==None):
        #try:
        self._client = MongoClient()
        self._db = self._client["airodb"]
        self.dumps = self._db.airodb_dumps
        #Fix: start a count command to force the client to connect
        self.dumps.count_documents({})
        #except pymongo.errors.ServerSelectionTimeoutError:
        #  print("Unable to connect to the local MongoDB instance")
        #  sys.exit(2)
      else:
        self._client = mongoClient
        self._db = self._client.airodb
        self.dumps = self._db.airodb_dumps

    def __del__(self): 
      self._client.close()

    def getSessionList(self):
        return self.dumps.aggregate([{"$match":{}}, {"$group": { "_id":"$SessionName", "first": { "$first": "$FirstTimeSeen"}, "last": { "$last": "$LastTimeSeen"}, "count": { "$sum": 1}}}])

    def getSessionAP(self, sessionName):
      retVal = []
      apList = self.dumps.aggregate([{"$match":{"SessionName":sessionName}}, {"$group": { "_id":"$BSSID", "name": { "$last": "$ESSID" }}}])
      for ap in apList:
        retVal.append(AccessPoint(MACAddress(ap["_id"]), ap["name"]))
      return retVal

    def getSessionAPStats(self, sessionName, apMACAddress):
      return self.dumps.aggregate([{"$match":{"SessionName":sessionName, "BSSID":apMACAddress}}, {
        "$group": { "_id":"$BSSID", 
        "name": { "$last": "$ESSID" }, 
        "FirstTimeSeen": { "$first": "$FirstTimeSeen"}, 
        "LastTimeSeen": { "$last": "$LastTimeSeen"},
        "Encryption": { "$last": "$Privacy"},
        "Cipher": { "$last": "$Cipher"},
        "Authentification": { "$last": "$Authentification"},
        "Channel": { "$last": "$Channel"},
        "Speed": { "$last": "$Speed"}
        }}])

    def getSessionAPRawLogs(self, sessionName, apMACAddress):
      return self.dumps.find({"SessionName":sessionName, "BSSID":apMACAddress})