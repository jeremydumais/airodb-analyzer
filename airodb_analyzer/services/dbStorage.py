import pymongo
import sys
from pymongo import MongoClient
from models.accessPoint import AccessPoint
from models.macAddress import MACAddress
from models.session import Session
from models.sessionAPStat import SessionAPStat
from datetime import datetime
from dateutil.parser import parse

class DBStorage():
    def __init__(self, mongoClient=None):
      if (mongoClient==None):
        #try:
        self._client = MongoClient()
        self._db = self._client["airodb"]
        self.dumps = self._db.airodb_dumps
        self.trusted_aps = self._db.airodb_trustedAP
        #Fix: start a count command to force the client to connect
        self.dumps.count_documents({})
        #except pymongo.errors.ServerSelectionTimeoutError:
        #  print("Unable to connect to the local MongoDB instance")
        #  sys.exit(2)
      else:
        self._client = mongoClient
        self._db = self._client.airodb
        self.dumps = self._db.airodb_dumps
        self.trusted_aps = self._db.airodb_trustedAP

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
      retVal = None
      stat = list(self.dumps.aggregate([{"$match":{"SessionName":sessionName, "BSSID":apMACAddress.getValue()}}, {
        "$group": { "_id":"$BSSID", 
        "name": { "$last": "$ESSID" }, 
        "firstTimeSeen": { "$first": "$FirstTimeSeen"}, 
        "lastTimeSeen": { "$last": "$LastTimeSeen"},
        "encryption": { "$last": "$Privacy"},
        "cipher": { "$last": "$Cipher"},
        "authentification": { "$last": "$Authentification"},
        "channel": { "$last": "$Channel"},
        "speed": { "$last": "$Speed"},
        "powerMin": { "$min": "$Power"},
        "powerMax": { "$max": "$Power"},
        "powerAvg": { "$avg": "$Power"}
        }}]))
      assert(len(stat) == 0 or len(stat) == 1)
      if (len(stat) == 1):
        retVal = SessionAPStat.createFromDict(stat[0])
      return retVal

    def getSessionAPRawLogs(self, sessionName, apMACAddress):
      return self.dumps.find({"SessionName":sessionName, "BSSID":apMACAddress})

    def getTrustedAPList(self):
      retVal = []
      trustedAPs = self.trusted_aps.find().sort("BSSID", 1)
      for trustedAP in trustedAPs:
        retVal.append(MACAddress(trustedAP["BSSID"]))
      return retVal

    def isTrustedAPExist(self, macAddress):
      if (not isinstance(macAddress, MACAddress)):
        raise TypeError("macAddress")
      return (self.trusted_aps.count_documents({"BSSID": macAddress.getValue()}) > 0)

    def insertTrustedAP(self, macAddress):
      if (not isinstance(macAddress, MACAddress)):
          raise TypeError("macAddress")
      # Check if the MAC Address already exist
      if (self.isTrustedAPExist(macAddress)):
        raise RuntimeError(macAddress.getValue() + " already exist!")
      self.trusted_aps.insert_one({ "BSSID": macAddress.getValue()})

    def updateTrustedAP(self, macAddressOld, macAddressNew):
      if (not isinstance(macAddressOld, MACAddress)):
        raise TypeError("macAddressOld")
      if (not isinstance(macAddressNew, MACAddress)):
        raise TypeError("macAddressNew")
      # Check if the MAC Address exist
      if (not(self.isTrustedAPExist(macAddressOld))):
        raise RuntimeError(macAddressOld.getValue() + " doesn't exist!")
      # Check if the new MAC Address already exist and is not the old one
      if (self.isTrustedAPExist(macAddressNew) and macAddressOld != macAddressNew):
        raise RuntimeError(macAddressNew.getValue() + " already exist!")
      self.trusted_aps.update_one({"BSSID": macAddressOld.getValue()}, 
        {"$set": {"BSSID": macAddressNew.getValue()}})
    
    def deleteTrustedAP(self, macAddress):
      if (not isinstance(macAddress, MACAddress)):
          raise TypeError("macAddress")
      # Check if the MAC Address exist
      if (not(self.isTrustedAPExist(macAddress))):
        raise RuntimeError(macAddress.getValue() + " doesn't exist!")
      self.trusted_aps.delete_one({"BSSID": macAddress.getValue()})

