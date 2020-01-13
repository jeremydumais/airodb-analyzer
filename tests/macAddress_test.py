import unittest
from os import path
import sys
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), 'airodb_analyzer'))
from models.macAddress import MACAddress

class TestMACAddressMethods(unittest.TestCase):
    def test_constructor_TestWithNoneValue_ThrowTypeError(self):
        with self.assertRaises(TypeError):
            MACAddress(None)

    def test_constructor_TestWithEmptyValue_ThrowValueError(self):
        with self.assertRaises(ValueError):
            MACAddress("")

    def test_constructor_TestWithOnlySpacesValue_ThrowValueError(self):
        with self.assertRaises(ValueError):
            MACAddress("   ")

    def test_constructor_TestWithInvalidMACAddressValue_ThrowValueError(self):
        with self.assertRaises(ValueError):
            MACAddress("12:34:56:78:89:HH")

    def test_constructor_TestWithValidMACAddressValue_ReturnValid(self):
            MACAddress("12:34:56:78:89:FF")

    def test_constructor_TestWithValidMACAddressValueLowercase_ReturnValid(self):
            MACAddress("12:aa:56:bb:89:FF")

    def test_constructor_TestWithEmptyMACAddressValue_ThrowValueError(self):
        with self.assertRaises(ValueError):
            MACAddress(":::::")

    def test_constructor_TestWithEmptyTooLongMACAddressValue_ThrowValueError(self):
        with self.assertRaises(ValueError):
            MACAddress("::::::")

    def test_getValue_TestWith12AA56BB89FF_Return12AA56BB89FF(self):
            expected = "12:AA:56:BB:89:FF"
            macAddr = MACAddress(expected)
            self.assertEqual(expected, macAddr.getValue())
    
    def test_getValue_TestWith12aa56bb89FFWithLowerChars_Return12aa56bb89FF(self):
        expected = "12:AA:56:BB:89:FF"
        macAddr = MACAddress("12:aa:56:bb:89:FF")
        self.assertEqual(expected, macAddr.getValue())

    def test_setValue_TestWithNoneValue_ThrowTypeError(self):
        macAddr = MACAddress("12:aa:56:bb:89:FF")
        with self.assertRaises(TypeError):
            macAddr.setValue(None)

    def test_setValue_TestWithEmptyValue_ThrowValueError(self):
        macAddr = MACAddress("12:aa:56:bb:89:FF")
        with self.assertRaises(ValueError):
            macAddr.setValue("")

    def test_setValue_TestWithOnlySpacesValue_ThrowValueError(self):
        macAddr = MACAddress("12:aa:56:bb:89:FF")
        with self.assertRaises(ValueError):
            macAddr.setValue("   ")

    def test_setValue_TestWithInvalidMACAddressValue_ThrowValueError(self):
        macAddr = MACAddress("12:aa:56:bb:89:FF")
        with self.assertRaises(ValueError):
            macAddr.setValue("12:34:56:78:89:HH")

    def test_setValue_TestWithValidMACAddressValue_ReturnValid(self):
        macAddr = MACAddress("12:aa:56:bb:89:FF")
        macAddr.setValue("12:34:56:78:89:FF")
        self.assertEqual("12:34:56:78:89:FF", macAddr.getValue())


    def test_setValue_TestWithValidMACAddressValueLowercase_ReturnValid(self):
        macAddr = MACAddress("12:aa:56:bb:89:FF")
        macAddr.setValue("12:aa:56:bb:88:FF")
        self.assertEqual("12:AA:56:BB:88:FF", macAddr.getValue())


    def test_setValue_TestWithEmptyMACAddressValue_ThrowValueError(self):
        macAddr = MACAddress("12:aa:56:bb:89:FF")
        with self.assertRaises(ValueError):
            macAddr.setValue(":::::")

    def test_equalityOperator_TestWithIdenticalValues_ReturnTrue(self):
        macAddr1 = MACAddress("12:aa:56:bb:89:FF")
        macAddr2 = MACAddress("12:aa:56:bb:89:FF")
        self.assertEqual(macAddr1, macAddr2)
        
    def test_equalityOperator_TestWithDifferentValues_ReturnFalse(self):
        macAddr1 = MACAddress("12:aa:56:bb:89:FE")
        macAddr2 = MACAddress("12:aa:56:bb:89:FF")
        self.assertFalse(macAddr1 == macAddr2)

    def test_equalityOperator_TestWithAnotherType_ReturnFalse(self):
        self.assertNotEqual(MACAddress("12:aa:56:bb:89:FE"), 3)
    
    def test_inequalityOperator_TestWithDifferentValues_ReturnTrue(self):
        macAddr1 = MACAddress("12:aa:56:bb:89:FE")
        macAddr2 = MACAddress("12:aa:56:bb:89:FF")
        self.assertTrue(macAddr1 != macAddr2)

    def test_inequalityOperator_TestWithIdenticalValues_ReturnFalse(self):
        macAddr1 = MACAddress("12:aa:56:bb:89:FF")
        macAddr2 = MACAddress("12:aa:56:bb:89:FF")
        self.assertFalse(macAddr1 != macAddr2)

    def test_hashOperator_TestWithDifferentValues_ReturnDifferentHash(self):
        macAddr1 = MACAddress("12:aa:56:bb:89:FE")
        macAddr2 = MACAddress("12:aa:56:bb:89:FF")
        self.assertNotEqual(hash(macAddr1), hash(macAddr2))       

    def test_hashOperator_TestWithIdenticalValues_ReturnSameHash(self):
        macAddr1 = MACAddress("12:aa:56:bb:89:FF")
        macAddr2 = MACAddress("12:aa:56:bb:89:FF")
        self.assertEqual(hash(macAddr1), hash(macAddr2))    