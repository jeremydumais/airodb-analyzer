from models.macAddress import MACAddress

class AccessPoint():
    _macAddress = None
    _name = None

    def __init__(self, macAddress, name):
        if (not isinstance(macAddress, MACAddress)):
            raise TypeError("macAddress")
        if (not isinstance(name, str)):
            raise TypeError("name")
        self._macAddress = macAddress
        self._name = name

    def getMACAddress(self):
        return self._macAddress

    def getName(self):
        return self._name
    
    def setMACAddress(self, macAddress):
        if (not isinstance(macAddress, MACAddress)):
            raise TypeError("macAddress")
        self._macAddress = macAddress 

    def setName(self, name):
        if (not isinstance(name, str)):
            raise TypeError("name")
        self._name = name

    def __eq__(self, other):
        if isinstance(other, AccessPoint):
            return (self._macAddress == other._macAddress and 
                self._name == other._name)
        return False

    def __hash__(self):
        return hash((self._macAddress, self._name))