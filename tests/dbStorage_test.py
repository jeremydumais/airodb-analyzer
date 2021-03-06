import unittest
from os import path
import sys
from mongomock import MongoClient
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'airodb_analyzer'))
from services.dbStorage import DBStorage
from models.accessPoint import AccessPoint
from models.macAddress import MACAddress
from models.session import Session
from models.sessionAPStat import SessionAPStat
from datetime import datetime

class TestDBStorageMethods_OneDumpEntryFixture(unittest.TestCase):
    def setUp(self):
        self.mockClient = MongoClient()
        entries = [{
            "BSSID" : "64:70:02:63:0E:86",
            "FirstTimeSeen": "2019-10-30 14:31:34",
            "LastTimeSeen": "2019-10-30 14:31:56", 
            "Privacy": "WPA2",
            "Cipher": "CCMP",
            "Authentification": "PSK",
            "Power": -24,
            "Channel": 6,
            "Speed": 54,
            "ESSID" : "myAP",
            "SessionName": "MySession",
        }]
        self.mockClient.airodb.airodb_dumps.insert_many(entries)

    def tearDown(self):
        self.mockClient.close()

    def test_getSessionAP_TestWithValidSessionName_Return1AP(self):
        dbStorage = DBStorage(self.mockClient)
        expected = AccessPoint(MACAddress("64:70:02:63:0E:86"), "myAP")
        apList = list(dbStorage.getSessionAP("MySession"))
        self.assertEqual(1, len(apList))
        self.assertEqual(expected, apList[0])

    def test_getSessionAP_TestWithNonExistantSessionName_Return0AP(self):
        dbStorage = DBStorage(self.mockClient)
        expected = AccessPoint(MACAddress("64:70:02:63:0E:86"), "myAP")
        apList = list(dbStorage.getSessionAP("MyNonExistantSession"))
        self.assertEqual(0, len(apList))

    def test_getSessionList_Return1Session(self):
        dbStorage = DBStorage(self.mockClient)
        expected = Session("MySession", datetime(2019,10,30,14,31,34), datetime(2019,10,30,14,31,56), 1)
        sessions = dbStorage.getSessionList()
        self.assertEqual(1, len(sessions))
        self.assertEqual(expected, sessions[0])

    def test_getSessionAPStats_TestWithValidMACAndSession_Return1APStat(self):
        dbStorage = DBStorage(self.mockClient)
        apStat = dbStorage.getSessionAPStats("MySession", MACAddress("64:70:02:63:0E:86"))
        self.assertIsNotNone(apStat)
        self.assertEqual("myAP", apStat.getName())
        self.assertEqual(MACAddress("64:70:02:63:0E:86"), apStat.getMACAddress())
        self.assertEqual(datetime(2019,10,30,14,31,34), apStat.getFirstTimeSeen())
        self.assertEqual(datetime(2019,10,30,14,31,56), apStat.getLastTimeSeen())
        self.assertEqual("WPA2", apStat.getEncryption())
        self.assertEqual("CCMP", apStat.getCipher())
        self.assertEqual("PSK", apStat.getAuthentification())
        self.assertEqual(6, apStat.getChannel())
        self.assertEqual(54, apStat.getSpeed())
        self.assertEqual(-24, apStat.getPowerLevelMin())
        self.assertEqual(-24, apStat.getPowerLevelMax())
        self.assertEqual(-24, apStat.getPowerLevelAvg())

    def test_getSessionAPStats_TestWithNonExistantMAC_ReturnNone(self):
        dbStorage = DBStorage(self.mockClient)
        apStat = dbStorage.getSessionAPStats("MySession", MACAddress("14:70:02:63:0E:86"))
        self.assertIsNone(apStat)

    def test_getSessionAPStats_TestWithNonExistantSession_ReturnNone(self):
        dbStorage = DBStorage(self.mockClient)
        apStat = dbStorage.getSessionAPStats("MySession44", MACAddress("64:70:02:63:0E:86"))
        self.assertIsNone(apStat)

class TestDBStorageMethods_FourDumpEntriesFixture(unittest.TestCase):
    def setUp(self):
        self.mockClient = MongoClient()
        entries = [{
            "BSSID" : "64:70:02:63:0E:86",
            "FirstTimeSeen": "2019-10-30 14:31:34",
            "LastTimeSeen": "2019-10-30 14:31:56", 
            "Privacy": "WPA2",
            "Cipher": "CCMP",
            "Authentification": "PSK",
            "Power": -26,
            "Channel": 6,
            "Speed": 54,
            "ESSID" : "myAP",
            "SessionName": "MySession",
        },
        {
            "BSSID" : "64:70:02:63:0E:86",
            "FirstTimeSeen": "2019-10-30 14:31:34",
            "LastTimeSeen": "2019-10-30 14:32:01", 
            "Privacy": "WPA2",
            "Cipher": "CCMP",
            "Authentification": "PSK",
            "Power": -30,
            "Channel": 6,
            "Speed": 54,
            "ESSID" : "myAP",
            "SessionName": "MySession",
        },
        {
            "BSSID" : "54:70:02:63:0E:82",
            "FirstTimeSeen": "2019-10-30 14:31:38",
            "LastTimeSeen": "2019-10-30 14:32:06", 
            "Privacy": "WEP",
            "Cipher": "WEP40",
            "Authentification": "OPN",
            "Power": -52,
            "Channel": 6,
            "Speed": 54,
            "ESSID" : "myAP1",
            "SessionName": "MySession",
        },
        {
            "BSSID" : "44:70:02:63:0E:81",
            "FirstTimeSeen": "2019-10-31 09:31:37",
            "LastTimeSeen": "2019-10-31 09:32:21", 
            "Privacy": "OPN",
            "Cipher": "",
            "Authentification": "",
            "Power": -80,
            "Channel": 11,
            "Speed": 22,
            "ESSID" : "myAP2",
            "SessionName": "MySession2",
        }]
        self.mockClient.airodb.airodb_dumps.insert_many(entries)

    def tearDown(self):
        self.mockClient.close()

    def test_getSessionAP_TestWithMySession_Return2AP(self):
        dbStorage = DBStorage(self.mockClient)
        expected = [AccessPoint(MACAddress("64:70:02:63:0E:86"), "myAP"),
            AccessPoint(MACAddress("54:70:02:63:0E:82"), "myAP1")]
        apList = list(dbStorage.getSessionAP("MySession"))
        self.assertEqual(2, len(apList))
        for index in range(len(expected)):
            self.assertEqual(expected[index], apList[index])

    def test_getSessionAP_TestWithMySession2_Return1AP(self):
        dbStorage = DBStorage(self.mockClient)
        expected = AccessPoint(MACAddress("44:70:02:63:0E:81"), "myAP2")
        apList = list(dbStorage.getSessionAP("MySession2"))
        self.assertEqual(1, len(apList))
        self.assertEqual(expected, apList[0])

    def test_getSessionList_Return2Session(self):
        dbStorage = DBStorage(self.mockClient)
        expected = [Session("MySession", datetime(2019,10,30,14,31,34), datetime(2019,10,30,14,32,6), 3),
            Session("MySession2", datetime(2019,10,31,9,31,37), datetime(2019,10,31,9,32,21), 1)]
        sessions = dbStorage.getSessionList()
        self.assertEqual(2, len(sessions))
        for index in range(len(expected)):
            self.assertEqual(expected[index], sessions[index])

    def test_getSessionAPStats_TestWithSessionOfTwoEntries_Return1APStat(self):
        dbStorage = DBStorage(self.mockClient)
        apStat = dbStorage.getSessionAPStats("MySession", MACAddress("64:70:02:63:0E:86"))
        self.assertIsNotNone(apStat)
        self.assertEqual("myAP", apStat.getName())
        self.assertEqual(MACAddress("64:70:02:63:0E:86"), apStat.getMACAddress())
        self.assertEqual(datetime(2019,10,30,14,31,34), apStat.getFirstTimeSeen())
        self.assertEqual(datetime(2019,10,30,14,32,1), apStat.getLastTimeSeen())
        self.assertEqual("WPA2", apStat.getEncryption())
        self.assertEqual("CCMP", apStat.getCipher())
        self.assertEqual("PSK", apStat.getAuthentification())
        self.assertEqual(6, apStat.getChannel())
        self.assertEqual(54, apStat.getSpeed())
        self.assertEqual(-30, apStat.getPowerLevelMin())
        self.assertEqual(-26, apStat.getPowerLevelMax())
        self.assertEqual(-28, apStat.getPowerLevelAvg())

    def test_getSessionAPStats_TestWithSessionOfOneEntry_Return1APStat(self):
        dbStorage = DBStorage(self.mockClient)
        apStat = dbStorage.getSessionAPStats("MySession", MACAddress("54:70:02:63:0E:82"))
        self.assertIsNotNone(apStat)
        self.assertEqual("myAP1", apStat.getName())
        self.assertEqual(MACAddress("54:70:02:63:0E:82"), apStat.getMACAddress())
        self.assertEqual(datetime(2019,10,30,14,31,38), apStat.getFirstTimeSeen())
        self.assertEqual(datetime(2019,10,30,14,32,6), apStat.getLastTimeSeen())
        self.assertEqual("WEP", apStat.getEncryption())
        self.assertEqual("WEP40", apStat.getCipher())
        self.assertEqual("OPN", apStat.getAuthentification())
        self.assertEqual(6, apStat.getChannel())
        self.assertEqual(54, apStat.getSpeed())
        self.assertEqual(-52, apStat.getPowerLevelMin())
        self.assertEqual(-52, apStat.getPowerLevelMax())
        self.assertEqual(-52, apStat.getPowerLevelAvg())

    def test_getSessionAPStats_TestWithNonExistantMAC_ReturnNone(self):
        dbStorage = DBStorage(self.mockClient)
        apStat = dbStorage.getSessionAPStats("MySession", MACAddress("14:70:02:63:0E:86"))
        self.assertIsNone(apStat)

    def test_getSessionAPStats_TestWithNonExistantSession_ReturnNone(self):
        dbStorage = DBStorage(self.mockClient)
        apStat = dbStorage.getSessionAPStats("MySession44", MACAddress("64:70:02:63:0E:86"))
        self.assertIsNone(apStat)

class TestDBStorageMethods_OneTrustedAPEntryFixture(unittest.TestCase):
    def setUp(self):
        self.mockClient = MongoClient()
        entries = [{
            "BSSID" : "64:70:02:63:0E:86"
        }]
        self.mockClient.airodb.airodb_trustedAP.insert_many(entries)

    def tearDown(self):
        self.mockClient.close()

    def test_getTrustedAPList_Return1AP(self):
        dbStorage = DBStorage(self.mockClient)
        expected = MACAddress("64:70:02:63:0E:86")
        trustedAPs = dbStorage.getTrustedAPList()
        self.assertEqual(1, len(trustedAPs))
        self.assertEqual(expected, trustedAPs[0])

    def test_insertTrustedAP_TestWithValidNonExistingMAC_ReturnSuccess(self):
        dbStorage = DBStorage(self.mockClient)
        dbStorage.insertTrustedAP(MACAddress("64:70:02:63:0E:87"))
        trustedAPs = dbStorage.getTrustedAPList()
        self.assertEqual(2, len(trustedAPs))
        self.assertEqual(MACAddress("64:70:02:63:0E:87"), trustedAPs[1])

    def test_insertTrustedAP_TestWithValidExistingMAC_ThrowRuntimeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(RuntimeError):
            dbStorage.insertTrustedAP(MACAddress("64:70:02:63:0E:86"))

    def test_insertTrustedAP_TestWithNoneMAC_ThrowTypeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(TypeError):
            dbStorage.insertTrustedAP(None)

    def test_insertTrustedAP_TestWithStringMAC_ThrowTypeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(TypeError):
            dbStorage.insertTrustedAP("2345")

    def test_isTrustedAPExist_TestWithNoneMACAddress_ThrowTypeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(TypeError):
            dbStorage.isTrustedAPExist(None)

    def test_isTrustedAPExist_TestWithStringMACAddress_ThrowTypeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(TypeError):
            dbStorage.isTrustedAPExist("64:70:02:63:0E:86")

    def test_isTrustedAPExist_TestWithExistantMACAddress_ReturnTrue(self):
        dbStorage = DBStorage(self.mockClient)
        self.assertTrue(dbStorage.isTrustedAPExist(MACAddress("64:70:02:63:0E:86")))
    
    def test_isTrustedAPExist_TestWithNonExistantMACAddress_ReturnFalse(self):
        dbStorage = DBStorage(self.mockClient)
        self.assertFalse(dbStorage.isTrustedAPExist(MACAddress("64:70:02:63:0E:85")))

    def test_updateTrustedAP_TestWithExistantOldAndNonExistanNew_ReturnSucces(self):
        dbStorage = DBStorage(self.mockClient)
        dbStorage.updateTrustedAP(MACAddress("64:70:02:63:0E:86"), MACAddress("64:70:02:63:0E:87"))
        trustedAPs = dbStorage.getTrustedAPList()
        self.assertEqual(1, len(trustedAPs))
        self.assertEqual(MACAddress("64:70:02:63:0E:87"), trustedAPs[0])

    def test_updateTrustedAP_TestWithExistantOldAndSameNew_ReturnSucces(self):
        dbStorage = DBStorage(self.mockClient)
        dbStorage.updateTrustedAP(MACAddress("64:70:02:63:0E:86"), MACAddress("64:70:02:63:0E:86"))
        trustedAPs = dbStorage.getTrustedAPList()
        self.assertEqual(1, len(trustedAPs))
        self.assertEqual(MACAddress("64:70:02:63:0E:86"), trustedAPs[0])

    def test_updateTrustedAP_TestWithNonExistantOld_ThrowRuntimeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(RuntimeError):
            dbStorage.updateTrustedAP(MACAddress("64:70:02:63:0E:87"), MACAddress("64:70:02:63:0E:86"))
    
    def test_updateTrustedAP_TestWithExistantNewAndNotTheOld_ThrowRuntimeError(self):
        dbStorage = DBStorage(self.mockClient)
        dbStorage.insertTrustedAP(MACAddress("64:70:02:63:0E:87"))
        with self.assertRaises(RuntimeError):
            dbStorage.updateTrustedAP(MACAddress("64:70:02:63:0E:87"), MACAddress("64:70:02:63:0E:86"))

    def test_updateTrustedAP_TestWithNoneMACOld_ThrowTypeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(TypeError):
            dbStorage.updateTrustedAP(None, MACAddress("64:70:02:63:0E:86"))
   
    def test_updateTrustedAP_TestWithStringMACOld_ThrowTypeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(TypeError):
            dbStorage.updateTrustedAP("64:70:02:63:0E:86", MACAddress("64:70:02:63:0E:86"))

    def test_updateTrustedAP_TestWithNoneMACNew_ThrowTypeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(TypeError):
            dbStorage.updateTrustedAP(MACAddress("64:70:02:63:0E:86"), None)
   
    def test_updateTrustedAP_TestWithStringMACNew_ThrowTypeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(TypeError):
            dbStorage.updateTrustedAP(MACAddress("64:70:02:63:0E:86"), "64:70:02:63:0E:86")

    def test_deleteTrustedAP_TestWithExistingMAC_ReturnSuccess(self):
        dbStorage = DBStorage(self.mockClient)
        dbStorage.deleteTrustedAP(MACAddress("64:70:02:63:0E:86"))
        trustedAPs = dbStorage.getTrustedAPList()
        self.assertEqual(0, len(trustedAPs))

    def test_deleteTrustedAP_TestWithNoneMAC_ThrowTypeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(TypeError):
            dbStorage.deleteTrustedAP(None)

    def test_deleteTrustedAP_TestWithStringMAC_ThrowTypeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(TypeError):
            dbStorage.deleteTrustedAP("64:70:02:63:0E:86")

    def test_deleteTrustedAP_TestWithNonExistantMAC_ThrowRuntimeError(self):
        dbStorage = DBStorage(self.mockClient)
        with self.assertRaises(RuntimeError):
            dbStorage.deleteTrustedAP(MACAddress("64:70:02:63:0E:87"))