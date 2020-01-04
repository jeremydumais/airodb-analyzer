import pymongo
import sys
from pymongo import MongoClient

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
      return self.dumps