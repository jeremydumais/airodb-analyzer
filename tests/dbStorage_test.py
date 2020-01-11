import unittest
from os import path
import sys
from mongomock import MongoClient
from airodb_analyzer.services.dbStorage import DBStorage
from airodb_analyzer.models.accessPoint import AccessPoint
from airodb_analyzer.models.macAddress import MACAddress

class TestDBStorageMethods_OneEntryFixture(unittest.TestCase):
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