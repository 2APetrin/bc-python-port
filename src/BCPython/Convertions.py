from py4j.java_gateway import JavaObject
from decimal import Decimal
from typing import Any, Dict, List
from typing import Optional


# py4j converts byte[] into bytes on its own, but write it just in case
def is_java_proxy(obj: Any) -> bool:
    return isinstance(obj, JavaObject)


def java_bytes_to_bytes(jbytes) -> bytes:
    return bytes(str(jbytes), "utf-8")


def java_collection_to_list(jcol, gateway=None) -> List[Any]:
    if isinstance(jcol, (list, tuple, set)):
        return [java_to_py(x, gateway) for x in jcol]

    if isinstance(jcol, (bytes, bytearray)):
        return list(java_bytes_to_bytes(jcol))

    try:
        return [java_to_py(x, gateway) for x in jcol]
    except Exception:
        return [java_to_py(jcol, gateway)]


def java_map_to_dict(jmap, gateway=None) -> Optional[Dict[Any, Any]]:
    res = {}
    try:
        # Если proxy поддерживает items()
        for entry in jmap.items():
            k, v = entry[0], entry[1]
            res[java_to_py(k, gateway)] = java_to_py(v, gateway)
        return res
    except Exception:
        pass
    try:
        # entrySet или keySet
        for entry in jmap.entrySet():
            k = entry.getKey()
            v = entry.getValue()
            res[java_to_py(k, gateway)] = java_to_py(v, gateway)
        return res
    except Exception:
        pass
    try:
        for k in jmap.keySet():
            res[java_to_py(k, gateway)] = java_to_py(jmap.get(k), gateway)
        return res
    except Exception:
        pass
    return {}


def java_enum_to_str(enum_proxy) -> str:
    try:
        return enum_proxy.name()
    except Exception:
        return str(enum_proxy)


def java_bigdecimal_to_decimal(jbd) -> Optional[Decimal]:
    if jbd is None:
        return None

    try:
        return Decimal(str(jbd.toString()))
    except Exception:
        try:
            return Decimal(str(jbd))
        except Exception:
            return None


def java_biginteger_to_int(jbi) -> Optional[int]:
    if jbi is None:
        return None

    try:
        return int(jbi.toString())
    except Exception:
        try:
            return int(str(jbi))
        except Exception:
            return None


def java_to_py(obj: Any, gateway) -> Any:
    java_to_py.Iterable = gateway.jvm.java.lang.Class.forName("java.lang.Iterable")

    if obj is None:
        return None

    if isinstance(obj, (bool, int, float, str, bytes, bytearray)):
        return obj

    if not is_java_proxy(obj):
        if isinstance(obj, dict):
            return {java_to_py(k, gateway): java_to_py(v, gateway) for k, v in obj.items()}
        if isinstance(obj, set):
            return {java_to_py(x, gateway) for x in obj}
        if isinstance(obj, (list, tuple)):
            return [java_to_py(x, gateway) for x in obj]
        return obj

    try:
        jclass = obj.getClass()
        cname = jclass.getName()
    except Exception:
        jclass = None
        cname = ""

    # Enum -> имя
    if jclass and jclass.isEnum():
        return java_enum_to_str(obj)
    # byte[] (Java) -> bytes (Python):contentReference[oaicite:4]{index=4}
    if cname == "[B":
        return java_bytes_to_bytes(obj)
    # BigDecimal / BigInteger -> Decimal / int
    if cname.endswith("BigDecimal"):
        return java_bigdecimal_to_decimal(obj)
    if cname.endswith("BigInteger"):
        return java_biginteger_to_int(obj)
    # Map -> dict
    if cname.endswith("Map"):
        return java_map_to_dict(obj, gateway)
    # Collection/Array -> list
    objclass = obj.getClass()
    if objclass.isArray() or java_to_py.Iterable.isAssignableFrom(objclass):
        return java_collection_to_list(obj, gateway)
    return obj
