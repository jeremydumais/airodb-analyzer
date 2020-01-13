import unittest
from os import path
import sys
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'airodb_analyzer'))
from models.accessPoint import AccessPoint
from models.macAddress import MACAddress

class TestAccessPointMethods(unittest.TestCase):
    def test_constructor_TestWithNoneMacAddress_ThrowTypeError(self):
        with self.assertRaises(TypeError):
            AccessPoint(None, None)

    def test_constructor_TestWithStringMacAddress_ThrowTypeError(self):
        with self.assertRaises(TypeError):
            AccessPoint("12:34:56:78:89:FF", None)
    
    def test_constructor_TestWithNoneName_ThrowTypeError(self):
        with self.assertRaises(TypeError):
            AccessPoint(MACAddress("12:34:56:78:89:FF"), None)

    def test_constructor_TestWithEmptyName_ReturnValid(self):
        AccessPoint(MACAddress("12:34:56:78:89:FF"), "")

    def test_constructor_TestWithValidMACAndName_ReturnValid(self):
        AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")

    def test_getMACAddress_TestWith1234567889FF_Return1234567889FF(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        expected = MACAddress("12:34:56:78:89:FF")
        self.assertEqual(expected, ap.getMACAddress())

    def test_getName_TestWithMyAP_ReturnMyAP(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        expected = "MyAP"
        self.assertEqual(expected, ap.getName())

    def test_setMACAddress_TestWithNoneMacAddress_ThrowTypeError(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        with self.assertRaises(TypeError):
            ap.setMACAddress(None)

    def test_setMACAddress_TestWithStringMacAddress_ThrowTypeError(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        with self.assertRaises(TypeError):
            ap.setMACAddress("12:34:56:78:89:FF")
    
    def test_setMACAddress_TestWithValidMAC_ReturnValid(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        ap.setMACAddress(MACAddress("12:34:56:77:89:FF"))
        self.assertEqual(ap.getMACAddress(), MACAddress("12:34:56:77:89:FF"))

    def test_setName_TestWithNoneName_ThrowTypeError(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        with self.assertRaises(TypeError):
            ap.setName(None)

    def test_setName_TestWithEmptyName_ReturnValid(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        ap.setName("")
        self.assertEqual(ap.getName(), "")

    def test_setName_TestWithNonEmptyName_ReturnValid(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        ap.setName("abc")
        self.assertEqual(ap.getName(), "abc")

    def test_equalityOperator_TestWithIdenticalValues_ReturnTrue(self):
        ap1 = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        ap2 = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        self.assertEqual(ap1, ap2)

    def test_equalityOperator_TestWithDifferentMAC_ReturnTrue(self):
        ap1 = AccessPoint(MACAddress("12:34:56:78:89:FE"), "MyAP")
        ap2 = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        self.assertNotEqual(ap1, ap2)

    def test_equalityOperator_TestWithDifferentName_ReturnTrue(self):
        ap1 = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP1")
        ap2 = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        self.assertNotEqual(ap1, ap2)

    def test_equalityOperator_TestWithDifferentMACAndName_ReturnTrue(self):
        ap1 = AccessPoint(MACAddress("12:34:56:78:89:FE"), "MyAP1")
        ap2 = AccessPoint(MACAddress("12:34:56:78:89:FF"), "MyAP")
        self.assertNotEqual(ap1, ap2)

    def test_equalityOperator_TestWithAnotherType_ReturnFalse(self):
        self.assertNotEqual(AccessPoint(MACAddress("12:34:56:78:89:FE"), "MyAP1"), 3)

    def test_isHidden_TestWithEmptyName_ReturnTrue(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FE"), "")
        self.assertTrue(ap.isHidden())

    def test_isHidden_TestWithOneX00Name_ReturnTrue(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FE"), "\\x00")
        self.assertTrue(ap.isHidden())

    def test_isHidden_TestWithTwoX00Name_ReturnTrue(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FE"), "\\x00\\x00")
        self.assertTrue(ap.isHidden())

    def test_isHidden_TestWithThreeX00Name_ReturnTrue(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FE"), "\\x00\\x00\\x00")
        self.assertTrue(ap.isHidden())

    def test_isHidden_TestWithValidName_ReturnFalse(self):
        ap = AccessPoint(MACAddress("12:34:56:78:89:FE"), "Home")
        self.assertFalse(ap.isHidden())

    def test_hashOperator_TestWithDifferentMAC_ReturnDifferentHash(self):
        ap1 = AccessPoint(MACAddress("12:34:56:78:89:FE"), "Home")
        ap2 = AccessPoint(MACAddress("12:34:56:78:89:FF"), "Home")
        self.assertNotEqual(hash(ap1), hash(ap2))       
    
    def test_hashOperator_TestWithDifferentName_ReturnDifferentHash(self):
        ap1 = AccessPoint(MACAddress("12:34:56:78:89:FE"), "Home")
        ap2 = AccessPoint(MACAddress("12:34:56:78:89:FF"), "Home1")
        self.assertNotEqual(hash(ap1), hash(ap2))   

    def test_hashOperator_TestWithIdenticalValues_ReturnSameHash(self):
        ap1 = AccessPoint(MACAddress("12:34:56:78:89:FE"), "Home")
        ap2 = AccessPoint(MACAddress("12:34:56:78:89:FE"), "Home")
        self.assertEqual(hash(ap1), hash(ap2))   