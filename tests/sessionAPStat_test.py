import unittest
from os import path
import sys
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'airodb_analyzer'))
from models.sessionAPStat import SessionAPStat
from models.macAddress import MACAddress
from datetime import datetime

class TestSessionAPStatMethods(unittest.TestCase):
    def test_constructor_TestDirectCall_ThrowAssertionError(self):
        with self.assertRaises(AssertionError):
            SessionAPStat("", "")

    def test_createFromDict_TestWithStringValue_ThrowTypeError(self):
        with self.assertRaises(TypeError):
            SessionAPStat.createFromDict("")

    def test_createFromDict_TestWithEmptyDict_ThrowValueError(self):
        with self.assertRaises(ValueError):
            SessionAPStat.createFromDict({})

    def test_createFromDict_TestWithOnlyName_ThrowValueError(self):
        with self.assertRaises(ValueError):
            SessionAPStat.createFromDict({"name" : "test"})

    def test_createFromDict_TestWithOnlyMACAddress_ThrowValueError(self):
        with self.assertRaises(ValueError):
            SessionAPStat.createFromDict({"_id" : "44:70:02:63:0E:81"})

    def test_createFromDict_TestWithBothNameAndMAC_ReturnValid(self):
        SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81"})

    def test_createFromDict_TestWithEmptyFirstTimeSeen_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": ""})
        self.assertEqual(None, session.getFirstTimeSeen())
        
    def test_createFromDict_TestWithValidFirstTimeSeen_ReturnValid(self):
        SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54"})

    def test_createFromDict_TestWithEmptyLastTimeSeen_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": ""})
        self.assertEqual(None, session.getLastTimeSeen())
        
    def test_createFromDict_TestWithValidLastTimeSeen_ReturnValid(self):
        SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "LastTimeSeen": "2020-01-03 15:24:54"})

    def test_createFromDict_TestWithNoEncryption_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": ""})
        self.assertEqual("", session.getEncryption())
        
    def test_createFromDict_TestWithValidEncryption_ReturnValid(self):
        SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-03 15:24:54",
            "encryption": "WPA2"})

    def test_createFromDict_TestWithNoCipher_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2"})
        self.assertEqual("", session.getCipher())
        
    def test_createFromDict_TestWithValidCipher_ReturnValid(self):
        SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-03 15:24:54",
            "encryption": "WPA2",
            "cipher": "CCMP"})

    def test_createFromDict_TestWithNoAuthentification_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP"})
        self.assertEqual("", session.getAuthentification())
        
    def test_createFromDict_TestWithValidAuthentification_ReturnValid(self):
        SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-03 15:24:54",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK"})

    def test_createFromDict_TestWithNoChannel_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK"})
        self.assertEqual(0, session.getChannel())

    def test_createFromDict_TestWithChannel6_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": 6})
        self.assertEqual(6, session.getChannel())

    def test_createFromDict_TestWithChannelNotInt_ReturnValid(self):
        with self.assertRaises(ValueError):
            SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "Test"})    

    def test_createFromDict_TestWithNoSpeed_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "6"})
        self.assertEqual(0, session.getSpeed())

    def test_createFromDict_TestWithSpeed54_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": 6,
            "speed": 54})
        self.assertEqual(54, session.getSpeed())
    
    def test_createFromDict_TestWithSpeedNotInt_ReturnValid(self):
        with self.assertRaises(ValueError):
            SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "6",
            "speed": "test"})    

    def test_createFromDict_TestWithNoPowerLevelMin_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "6",
            "speed": "54"})
        self.assertEqual(0, session.getPowerLevelMin())

    def test_createFromDict_TestWithPowerLevelMinMinus28_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": 6,
            "speed": 54,
            "powerMin": -28})
        self.assertEqual(-28, session.getPowerLevelMin())
    
    def test_createFromDict_TestWithPowerLevelMinNotInt_ReturnValid(self):
        with self.assertRaises(ValueError):
            SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "6",
            "speed": "test",
            "powerMin": "Test"})   

    def test_createFromDict_TestWithNoPowerLevelMax_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "6",
            "speed": "54",
            "powerMin": -24 })
        self.assertEqual(0, session.getPowerLevelMax())

    def test_createFromDict_TestWithPowerLevelMaxMinus28_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": 6,
            "speed": 54,
            "powerMin": -24,
            "powerMax": -28 })
        self.assertEqual(-28, session.getPowerLevelMax())
    
    def test_createFromDict_TestWithPowerLevelMaxNotInt_ReturnValid(self):
        with self.assertRaises(ValueError):
            SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "6",
            "speed": "test",
            "powerMin": -24,
            "powerMax": "Test" })   

    def test_createFromDict_TestWithNoPowerLevelAvg_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "6",
            "speed": "54",
            "powerMin": -24,
            "powerMax": -32 })
        self.assertEqual(0, session.getPowerLevelAvg())

    def test_createFromDict_TestWithPowerLevelAvgMinus28_ReturnValid(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": 6,
            "speed": 54,
            "powerMin": -24,
            "powerMax": -32,
            "powerAvg": -28 })
        self.assertEqual(-28, session.getPowerLevelAvg())
    
    def test_createFromDict_TestWithPowerLevelAvgNotInt_ReturnValid(self):
        with self.assertRaises(ValueError):
            SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "6",
            "speed": "test",
            "powerMin": -24,
            "powerMax": -32,
            "powerAvg": "Test"})   

    def test_getName_ReturnTest(self):
        session = SessionAPStat.createFromDict({"name" : "Test",
            "_id" : "44:70:02:63:0E:81"})
        self.assertEqual("Test", session.getName())
    
    def test_getMACAddress_ReturnValidMAC(self):
        session = SessionAPStat.createFromDict({"name" : "Test",
            "_id" : "44:70:02:63:0E:81"})
        expected = MACAddress("44:70:02:63:0E:81")
        self.assertEqual(expected, session.getMACAddress())

    def test_getFirstTimeSeen_ReturnValidDate(self):
        session = SessionAPStat.createFromDict({"name" : "Test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54"})
        expected = datetime(2020,1,2,13,24,54)
        self.assertEqual(expected, session.getFirstTimeSeen())

    def test_getLastTimeSeen_ReturnValidDate(self):
        session = SessionAPStat.createFromDict({"name" : "Test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-06 15:24:54"})
        expected = datetime(2020,1,6,15,24,54)
        self.assertEqual(expected, session.getLastTimeSeen())

    def test_getEncryption_ReturnWPA2(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-03 15:24:54",
            "encryption": "WPA2"})
        self.assertEqual("WPA2", session.getEncryption())
    
    def test_getCipher_ReturnCCMP(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-03 15:24:54",
            "encryption": "WPA2",
            "cipher": "CCMP"})
        self.assertEqual("CCMP", session.getCipher())
    
    def test_getAuthentification_ReturnPSK(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-03 15:24:54",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK"})
        self.assertEqual("PSK", session.getAuthentification())

    def test_getChannel_Return6(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-03 15:24:54",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "6"})
        self.assertEqual(6, session.getChannel())

    def test_getSpeed_Return54(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-03 15:24:54",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "6",
            "speed": "54"})
        self.assertEqual(54, session.getSpeed())

    def test_isProtected_TestWithEmptyEncryption_ReturnFalse(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-03 15:24:54",
            "encryption": "",
            "cipher": "",
            "authentification": "",
            "channel": "6",
            "speed": "54"})
        self.assertFalse(session.isProtected())

    def test_isProtected_TestWithOPNEncryption_ReturnFalse(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-03 15:24:54",
            "encryption": "OPN",
            "cipher": "",
            "authentification": "",
            "channel": "6",
            "speed": "54"})
        self.assertFalse(session.isProtected())  
    
    def test_isProtected_TestWithWPA2Encryption_ReturnTrue(self):
        session = SessionAPStat.createFromDict({"name" : "test",
            "_id" : "44:70:02:63:0E:81",
            "firstTimeSeen": "2020-01-02 13:24:54",
            "lastTimeSeen": "2020-01-03 15:24:54",
            "encryption": "WPA2",
            "cipher": "CCMP",
            "authentification": "PSK",
            "channel": "6",
            "speed": "54"})
        self.assertTrue(session.isProtected())