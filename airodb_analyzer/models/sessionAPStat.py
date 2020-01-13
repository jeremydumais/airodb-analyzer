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
        if ("channel" in value):
            if (self._isInt(value["channel"])):
                self._channel = int(value["channel"])
            else:
                raise ValueError("value")
        if ("speed" in value):
            if (self._isInt(value["speed"])):
                self._speed = int(value["speed"])
            else:
                raise ValueError("value")
        if ("powerMin" in value):
            if (self._isInt(value["powerMin"])):
                self._powerLevelMin = int(value["powerMin"])
            else:
                raise ValueError("value")
        if ("powerMax" in value):
            if (self._isInt(value["powerMax"])):
                self._powerLevelMax = int(value["powerMax"])
            else:
                raise ValueError("value")
        if ("powerAvg" in value):
            if (self._isInt(value["powerAvg"])):
                self._powerLevelAvg = int(value["powerAvg"])
            else:
                raise ValueError("value")
          
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

    def getChannel(self):
        return self._channel

    def getSpeed(self):
        return self._speed

    def getPowerLevelMin(self):
        return self._powerLevelMin

    def getPowerLevelMax(self):
        return self._powerLevelMax

    def getPowerLevelAvg(self):
        return self._powerLevelAvg

    def isProtected(self):
        return self._encryption != "" and self._encryption != "OPN"

    def _isInt(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False
