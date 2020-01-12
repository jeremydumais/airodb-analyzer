import unittest
from os import path
import sys
from mongomock import MongoClient
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'airodb_analyzer'))
from services.dbStorage import DBStorage
from models.accessPoint import AccessPoint
from models.macAddress import MACAddress
from models.session import Session
from datetime import datetime

class TestDBStorageMethods_OneDumpEntryFixture(unittest.TestCase):
    def setUp(self):
        self.mockClient = MongoClient()
        entries = [{
            "BSSID" : "64:70:02:63:0E:86",
            "FirstTimeSeen": "2019-10-30 14:31:34",
            "LastTimeSeen": "2019-10-30 14:31:56", 
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

class TestDBStorageMethods_ThreeDumpEntriesFixture(unittest.TestCase):
    def setUp(self):
        self.mockClient = MongoClient()
        entries = [{
            "BSSID" : "64:70:02:63:0E:86",
            "FirstTimeSeen": "2019-10-30 14:31:34",
            "LastTimeSeen": "2019-10-30 14:31:56", 
            "ESSID" : "myAP",
            "SessionName": "MySession",
        },
        {
            "BSSID" : "54:70:02:63:0E:82",
            "FirstTimeSeen": "2019-10-30 14:31:38",
            "LastTimeSeen": "2019-10-30 14:32:06", 
            "ESSID" : "myAP1",
            "SessionName": "MySession",
        },
        {
            "BSSID" : "44:70:02:63:0E:81",
            "FirstTimeSeen": "2019-10-31 09:31:37",
            "LastTimeSeen": "2019-10-31 09:32:21", 
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
        expected = [Session("MySession", datetime(2019,10,30,14,31,34), datetime(2019,10,30,14,32,6), 2),
            Session("MySession2", datetime(2019,10,31,9,31,37), datetime(2019,10,31,9,32,21), 1)]
        sessions = dbStorage.getSessionList()
        self.assertEqual(2, len(sessions))
        for index in range(len(expected)):
            self.assertEqual(expected[index], sessions[index])
