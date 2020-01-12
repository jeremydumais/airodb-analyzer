import pymongo
import sys
from pymongo import MongoClient
from models.accessPoint import AccessPoint
from models.macAddress import MACAddress
from models.session import Session
from datetime import datetime
from dateutil.parser import parse

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
        retVal = []
        sessions = self.dumps.aggregate([{"$match":{}}, 
          {"$group": { "_id":"$SessionName", 
            "first": { "$first": "$FirstTimeSeen"}, 
            "last": { "$last": "$LastTimeSeen"}, 
            "count": { "$sum": 1}}}, 
          {"$sort": {"name":1}}])
        for session in sessions:
          retVal.append(Session(session["_id"], 
            parse(session["first"]), 
            parse(session["last"]), 
            session["count"]))
        return retVal

    def getSessionAP(self, sessionName):
      retVal = []
      apList = self.dumps.aggregate([{"$match":{"SessionName":sessionName}}, 
        {"$group": { "_id":"$BSSID", 
          "name": { "$last": "$ESSID" }}}, 
        {"$sort": {"name":1}}])
      for ap in apList:
        retVal.append(AccessPoint(MACAddress(ap["_id"]), ap["name"]))
      return retVal

    def getSessionAPStats(self, sessionName, apMACAddress):
      return self.dumps.aggregate([{"$match":{"SessionName":sessionName, "BSSID":apMACAddress}}, {
        "$group": { "_id":"$BSSID", 
        "name": { "$last": "$ESSID" }, 
        "firstTimeSeen": { "$first": "$FirstTimeSeen"}, 
        "lastTimeSeen": { "$last": "$LastTimeSeen"},
        "encryption": { "$last": "$Privacy"},
        "cipher": { "$last": "$Cipher"},
        "authentification": { "$last": "$Authentification"},
        "channel": { "$last": "$Channel"},
        "speed": { "$last": "$Speed"}
        }}])

    def getSessionAPRawLogs(self, sessionName, apMACAddress):
      return self.dumps.find({"SessionName":sessionName, "BSSID":apMACAddress})