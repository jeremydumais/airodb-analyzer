from datetime import datetime

class Session():
    _name = ""
    _firstEntryDateTime = None
    _lastEntryDateTime = None
    _nbOfRawLogs = 0

    def __init__(self, name, firstEntryDateTime = None, 
        lastEntryDateTime = None, nbOfRawLogs = 0):
        if (not isinstance(name, str)):
            raise TypeError("name")
        if (name.strip()):
            self._name = name
        else:
            raise ValueError("name")

        if (firstEntryDateTime != None):
            if (not isinstance(firstEntryDateTime, datetime)):
                raise TypeError("firstEntryDateTime")
            else:
                self._firstEntryDateTime = firstEntryDateTime

        if (lastEntryDateTime != None):
            if (not isinstance(lastEntryDateTime, datetime)):
                raise TypeError("lastEntryDateTime")
            else:
                self._lastEntryDateTime = lastEntryDateTime

        if (not isinstance(nbOfRawLogs, int)):
            raise TypeError("nbOfRawLogs")
        if (nbOfRawLogs < 0):
            raise ValueError("nbOfRawLogs")
        else:
            self._nbOfRawLogs = nbOfRawLogs


    def getName(self):
        return self._name

    def getFirstEntryDateTime(self):
        return self._firstEntryDateTime

    def getLastEntryDateTime(self):
        return self._lastEntryDateTime

    def getNBOfRawLogs(self):
        return self._nbOfRawLogs

    def setName(self, name):
        if (not isinstance(name, str)):
            raise TypeError("name")
        if (name.strip()):
            self._name = name
        else:
            raise ValueError("name")

    def setFirstEntryDateTime(self, firstEntryDateTime):
        if (firstEntryDateTime != None):
            if (not isinstance(firstEntryDateTime, datetime)):
                raise TypeError("firstEntryDateTime")
            else:
                self._firstEntryDateTime = firstEntryDateTime
        else:
            self._firstEntryDateTime = None
    
    def setLastEntryDateTime(self, lastEntryDateTime):
        if (lastEntryDateTime != None):
            if (not isinstance(lastEntryDateTime, datetime)):
                raise TypeError("lastEntryDateTime")
            else:
                self._lastEntryDateTime = lastEntryDateTime
        else:
            self._lastEntryDateTime = None

    def setNBOfRawLogs(self, value):
        if (not isinstance(value, int)):
            raise TypeError("value")
        if (value < 0):
            raise ValueError("value")
        else:
            self._nbOfRawLogs = value

    def __eq__(self, other):
        if isinstance(other, Session):
            return (self._name == other._name and 
                self._firstEntryDateTime == other._firstEntryDateTime and
                self._lastEntryDateTime == other._lastEntryDateTime and
                self._nbOfRawLogs == other._nbOfRawLogs) 
        return False

    def __hash__(self):
        return hash((self._name,
            self._firstEntryDateTime,
            self._lastEntryDateTime,
            self._nbOfRawLogs))