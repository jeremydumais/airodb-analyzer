from models.macAddress import MACAddress
from datetime import datetime
from dateutil import parser

class SessionAPStat():
    _name = ""
    _macAddress = ""
    _firstTimeSeen = None
    _lastTimeSeen = None
    _encryption = ""
    _cipher = ""
    _authentification = ""
    _channel = 0
    _speed = 0
    _powerLevelMin = 0
    _powerLevelMax = 0
    _powerLevelAvg = 0
    __create_key = object()

    @classmethod
    def createFromDict(cls, value):
        return SessionAPStat(cls.__create_key, value)

    def __init__(self, create_key, value):
        assert(create_key == SessionAPStat.__create_key), \
            "SessionAPStat objects must be created using SessionAPStat.create"
        if (not isinstance(value, dict)):
            raise TypeError("value")
        if ("name" in value and "_id" in value):
            self._name = value["name"]
            self._macAddress = MACAddress(value["_id"])
        else:
            raise ValueError("value")
        if ("firstTimeSeen" in value and value["firstTimeSeen"].strip() != ""):
            self._firstTimeSeen = parser.parse(value["firstTimeSeen"])  
        if ("lastTimeSeen" in value and value["lastTimeSeen"].strip() != ""):
            self._lastTimeSeen = parser.parse(value["lastTimeSeen"])
        if ("encryption" in value and value["encryption"].strip() != ""):
            self._encryption = value["encryption"]
        if ("cipher" in value and value["cipher"].strip() != ""):
            self._cipher = value["cipher"]
        if ("authentification" in value and value["authentification"].strip() != ""):
            self._authentification = value["authentification"]

          
    def getName(self):
        return self._name

    def getMACAddress(self):
        return self._macAddress

    def getFirstTimeSeen(self):
        return self._firstTimeSeen

    def getLastTimeSeen(self):
        return self._lastTimeSeen
    
    def getEncryption(self):
        return self._encryption

    def getCipher(self):
        return self._cipher
    
    def getAuthentification(self):
        return self._authentification
