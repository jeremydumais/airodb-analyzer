class MACAddress():
    _value = None

    def __init__(self, value):
        if (not isinstance(value, str)):
            raise TypeError("value")
        if (self._isValid(value)):
            self._value = value.upper()
        else:
            raise ValueError("value")
    
    def _isValid(self, macAddress): 
        sanitizedMACAddress = macAddress.strip().upper()
        if sanitizedMACAddress == "":
            return False
        
        #Ensure that we have 6 sections
        items = sanitizedMACAddress.split(":")
        if len(items) != 6:
            return False
        
        #Ensure that every section of the MAC Address has 2 characters
        for section in items:
            if len(section) != 2:
                return False

        #Ensure that all characters is hexadecimal
        HEXADECIMAL_CHARS = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
        for section in items:
            for character in section:
                if character not in HEXADECIMAL_CHARS:
                    return False
        
        return True

    def getValue(self):
        return self._value

    def setValue(self, value):
        if (not isinstance(value, str)):
            raise TypeError("value")
        if (self._isValid(value)):
            self._value = value.upper()
        else:
            raise ValueError("value")

    def __eq__(self, other):
        if isinstance(other, MACAddress):
            return self._value == other._value
        return False

    def __hash__(self):
        return hash((self._value))
