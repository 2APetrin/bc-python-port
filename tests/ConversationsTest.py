from BCPython.BCWrapper import get_gateway
from BCPython.Convertions import java_to_py, is_java_proxy
import unittest
from decimal import Decimal


class _ConvertionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gw = get_gateway()

    def test_simple_run(self):
        security = self.gw.jvm.java.security
        Security = security.Security
        BouncyCastleProvider = self.gw.jvm.org.bouncycastle.jce.provider.BouncyCastleProvider
        Security.addProvider(BouncyCastleProvider())

        text_bytes = "hash me please".encode("utf-8")

        MessageDigest = security.MessageDigest
        digest = MessageDigest.getInstance("SHA-256", "BC")
        hash_bytes = digest.digest(text_bytes)
        self.assertEqual(
            hash_bytes,
            b'\x8b\xa5\x88\x0e_\xa8xX,\x92\x110.0\x9f7\x99\xdbo\x83Hig\xbbt46\xfeO3\xde\x03'
        )

    def test_is_java_proxy_bytes(self):
        security = self.gw.jvm.java.security
        Security = security.Security
        BouncyCastleProvider = self.gw.jvm.org.bouncycastle.jce.provider.BouncyCastleProvider
        Security.addProvider(BouncyCastleProvider())

        MessageDigest = security.MessageDigest
        text_bytes = "hash me please".encode("utf-8")

        digest = MessageDigest.getInstance("SHA-256", "BC")
        hash_bytes = digest.digest(text_bytes)
        self.assertFalse(is_java_proxy(hash_bytes))
        self.assertTrue(type(hash_bytes) is bytes)

    def test_is_java_proxy_bigint(self):
        asn1 = self.gw.jvm.org.bouncycastle.asn1
        self.assertTrue(is_java_proxy(asn1.ASN1Integer(100).getValue()))
        self.assertTrue(type(java_to_py(asn1.ASN1Integer(100).getValue(), self.gw)) is int)

    def test_java_collection_to_list(self):
        # ArrayList -> list of strings
        ArrayList = self.gw.jvm.java.util.ArrayList
        al = ArrayList()
        al.add("one")
        al.add("two")
        py_list = java_to_py(al, self.gw)
        self.assertIsInstance(py_list, list)
        self.assertEqual(py_list, ["one", "two"])

        # HashSet -> list (order not guaranteed) -> compare as set
        HashSet = self.gw.jvm.java.util.HashSet
        hs = HashSet()
        hs.add("a")
        hs.add("b")
        py_list_set = java_to_py(hs, self.gw)
        self.assertIsInstance(py_list_set, list)
        self.assertEqual(set(py_list_set), {"a", "b"})

        # Java String[] array -> list
        jarr = self.gw.new_array(self.gw.jvm.java.lang.String, 2)
        jarr[0] = "x"
        jarr[1] = "y"
        py_from_array = java_to_py(jarr, self.gw)
        self.assertIsInstance(py_from_array, list)
        self.assertEqual(py_from_array, ["x", "y"])

    def test_java_map_to_dict(self):
        HashMap = self.gw.jvm.java.util.HashMap
        hm = HashMap()
        hm.put("k1", "v1")
        hm.put("k2", "v2")
        py_map = java_to_py(hm, self.gw)
        self.assertIsInstance(py_map, dict)
        self.assertEqual(py_map, {"k1": "v1", "k2": "v2"})

    def test_enum_and_numeric_conversions(self):
        # Enum (java.time.DayOfWeek)
        dow = self.gw.jvm.java.time.DayOfWeek.MONDAY
        name = java_to_py(dow, self.gw)
        self.assertEqual(name, "MONDAY")

        # BigDecimal -> Decimal
        bd = self.gw.jvm.java.math.BigDecimal("1234.5678")
        py_bd = java_to_py(bd, self.gw)
        self.assertIsInstance(py_bd, Decimal)
        self.assertEqual(py_bd, Decimal("1234.5678"))

        # BigInteger -> int
        bi = self.gw.jvm.java.math.BigInteger("12345678901234567890")
        py_bi = java_to_py(bi, self.gw)
        self.assertIsInstance(py_bi, int)
        self.assertEqual(py_bi, 12345678901234567890)

    def test_byte_array_conversion(self):
        Array = self.gw.jvm.java.lang.reflect.Array
        jbytes = self.gw.new_array(self.gw.jvm.byte, 3)
        Array.setByte(jbytes, 0, 1)
        Array.setByte(jbytes, 1, 2)
        Array.setByte(jbytes, 2, 3)
        py_bytes = java_to_py(jbytes, self.gw)
        self.assertIsInstance(py_bytes, (bytes, bytearray))

    def test_python_collections_passthrough(self):
        py_input = {
            "numbers": [1, 2, 3],
            "set": {4, 5},
            "nested": {"a": "b"}
        }
        converted = java_to_py(py_input, self.gw)
        self.assertIsInstance(converted, dict)
        self.assertEqual(converted["numbers"], [1, 2, 3])
        self.assertEqual(set(converted["set"]), {4, 5})
        self.assertEqual(converted["nested"], {"a": "b"})


if __name__ == "__main__":
    unittest.main()
