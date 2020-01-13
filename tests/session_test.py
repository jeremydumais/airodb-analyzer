import unittest
from os import path
import sys
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'airodb_analyzer'))
from models.session import Session
from datetime import datetime

class TestSessionMethods(unittest.TestCase):
    def test_constructor_TestWithNoneName_ThrowTypeError(self):
        with self.assertRaises(TypeError):
            Session(None)

    def test_constructor_TestWithIntTypeName_ThrowTypeError(self):
        with self.assertRaises(TypeError):
            Session(2)

    def test_constructor_TestWithEmptyName_ThrowValueError(self):
        with self.assertRaises(ValueError):
            Session("")
    
    def test_constructor_TestWithWhiteSpacesName_ThrowValueError(self):
        with self.assertRaises(ValueError):
            Session("   ")

    def test_constructor_TestWithValidNameCase1_ReturnValid(self):
        session = Session("MySession")
        self.assertEqual("MySession", session.getName())

    def test_constructor_TestWithValidNameCase2_ReturnValid(self):
        session = Session("MySession1")
        self.assertEqual("MySession1", session.getName())

    def test_constructor_TestWithFirstEntryInt_ThrowTypeError(self):
        with self.assertRaises(TypeError):
            Session("test", 1)

    def test_constructor_TestWithFirstEntryValidDateTime_ReturnValid(self):
        session = Session("test", datetime(2020,1,1,12,0,0))
        self.assertEqual(datetime(2020,1,1,12,0,0), session.getFirstEntryDateTime())

    def test_constructor_TestWithLastEntryInt_ThrowTypeError(self):
        with self.assertRaises(TypeError):
            Session("test", None, 1)

    def test_constructor_TestWithLastEntryValidDateTime_ReturnValid(self):
        session = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,2,12,0,0))
        self.assertEqual(datetime(2020,1,2,12,0,0), session.getLastEntryDateTime())

    def test_constructor_TestWithNBOfRawLogsStr_ThrowTypeError(self):
        with self.assertRaises(TypeError):
            Session("test", None, None, "Test")

    def test_constructor_TestWithNBOfRawLogsNegative_ThrowTypeError(self):
        with self.assertRaises(ValueError):
            Session("test", None, None, -1)

    def test_constructor_TestWithNBOfRawLogsPositive_ReturnValid(self):
        session = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,2,12,0,0), 5)
        self.assertEqual(5, session.getNBOfRawLogs())

    def test_setName_TestWithNoneName_ThrowTypeError(self):
        session = Session("MySession")
        with self.assertRaises(TypeError):
            session.setName(None)

    def test_setName_TestWithIntTypeName_ThrowTypeError(self):
        session = Session("MySession")
        with self.assertRaises(TypeError):
            session.setName(2)

    def test_setName_TestWithEmptyName_ThrowValueError(self):
        session = Session("MySession")
        with self.assertRaises(ValueError):
            session.setName("")
    
    def test_setName_TestWithWhiteSpacesName_ThrowValueError(self):
        session = Session("MySession")
        with self.assertRaises(ValueError):
            session.setName("   ")

    def test_setName_TestWithValidName_ReturnValid(self):
        session = Session("MySession")
        expected = "MyRenamedSession"
        session.setName(expected)
        self.assertEqual(expected, session.getName())

    def test_setFirstEntryDateTime_TestWithInt_ThrowTypeError(self):
        session = Session("test", datetime(2020,1,1,12,0,0))
        with self.assertRaises(TypeError):
            session.setFirstEntryDateTime(1)

    def test_setFirstEntryDateTime_TestWithValidDateTime_ReturnValid(self):
        session = Session("test", datetime(2020,1,1,12,0,0))
        session.setFirstEntryDateTime(datetime(2020,1,2,12,0,0))
        self.assertEqual(datetime(2020,1,2,12,0,0), session.getFirstEntryDateTime())

    def test_setFirstEntryDateTime_TestWithNone_ReturnValid(self):
        session = Session("test", datetime(2020,1,1,12,0,0))
        session.setFirstEntryDateTime(None)
        self.assertEqual(None, session.getFirstEntryDateTime())
    
    def test_setLastEntryDateTime_TestWithInt_ThrowTypeError(self):
        session = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0))
        with self.assertRaises(TypeError):
            session.setLastEntryDateTime(1)

    def test_setLastEntryDateTime_TestWithValidDateTime_ReturnValid(self):
        session = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0))
        session.setLastEntryDateTime(datetime(2020,1,2,12,0,0))
        self.assertEqual(datetime(2020,1,2,12,0,0), session.getLastEntryDateTime())

    def test_setLastEntryDateTime_TestWithNone_ReturnValid(self):
        session = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0))
        session.setLastEntryDateTime(None)
        self.assertEqual(None, session.getLastEntryDateTime())

    def test_setNBOfRawLogs_TestWithString_ThrowTypeError(self):
        session = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        with self.assertRaises(TypeError):
            session.setNBOfRawLogs("test")

    def test_setNBOfRawLogs_TestWithNegativeInt_ThrowTypeError(self):
        session = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        with self.assertRaises(ValueError):
            session.setNBOfRawLogs(-5)

    def test_setNBOfRawLogs_TestWithPositiveInt_ReturnValid(self):
        session = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        session.setNBOfRawLogs(7)
        self.assertEqual(7, session.getNBOfRawLogs())

    def test_equalityOperator_TestWithIdenticalValues_ReturnTrue(self):
        session1 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        session2 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        self.assertEqual(session1, session2)

    def test_equalityOperator_TestWithDifferentName_ReturnFalse(self):
        session1 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        session2 = Session("test1", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        self.assertNotEqual(session1, session2)

    def test_equalityOperator_TestWithDifferentFirstEntryDateTime_ReturnFalse(self):
        session1 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        session2 = Session("test", datetime(2020,1,1,12,0,1), datetime(2020,1,3,12,0,0), 9)
        self.assertNotEqual(session1, session2)

    def test_equalityOperator_TestWithDifferentLastEntryDateTime_ReturnFalse(self):
        session1 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        session2 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,1), 9)
        self.assertNotEqual(session1, session2)    

    def test_equalityOperator_TestWithDifferentNBOfRawLogs_ReturnFalse(self):
        session1 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        session2 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 8)
        self.assertNotEqual(session1, session2)   

    def test_equalityOperator_TestWithAnotherType_ReturnFalse(self):
        session = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        self.assertNotEqual(session, 3)   

    def test_hashOperator_TestWithDifferentName_ReturnDifferentHash(self):
        session1 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        session2 = Session("test1", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        self.assertNotEqual(hash(session1), hash(session2))   

    def test_hashOperator_TestWithDifferentFirstEntryDateTime_ReturnDifferentHash(self):
        session1 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        session2 = Session("test", datetime(2020,1,1,12,0,1), datetime(2020,1,3,12,0,0), 9)
        self.assertNotEqual(hash(session1), hash(session2))   

    def test_hashOperator_TestWithDifferentLastEntryDateTime_ReturnDifferentHash(self):
        session1 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        session2 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,1), 9)
        self.assertNotEqual(hash(session1), hash(session2))  

    def test_hashOperator_TestWithDifferentNBOfRawLogs_ReturnDifferentHash(self):
        session1 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        session2 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 8)
        self.assertNotEqual(hash(session1), hash(session2))  

    def test_hashOperator_TestWithIdenticalValues_ReturnSameHash(self):
        session1 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        session2 = Session("test", datetime(2020,1,1,12,0,0), datetime(2020,1,3,12,0,0), 9)
        self.assertEqual(hash(session1), hash(session2))   
