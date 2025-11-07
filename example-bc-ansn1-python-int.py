from BCWrapper import get_gateway
from Convertions import java_to_py, is_java_proxy

gw = get_gateway()
asn1 = gw.jvm.org.bouncycastle.asn1

asn_int = asn1.ASN1Integer(123456789012)
bigint_proxy = asn_int.getValue()
print("is java proxy:", is_java_proxy(bigint_proxy))

py_int = java_to_py(bigint_proxy, gw)
print("Converted to Python int:", py_int, type(py_int))
