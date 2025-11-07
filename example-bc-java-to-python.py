from BCWrapper import get_gateway
from Convertions import java_to_py

gw = get_gateway()

ArrayList = gw.jvm.java.util.ArrayList
al = ArrayList()
al.add("one")
al.add("two")
py_list = java_to_py(al, gw)
print("ArrayList ->", py_list, type(py_list))

HashMap = gw.jvm.java.util.HashMap
hm = HashMap()
hm.put("k1", "v1")
hm.put("k2", "v2")
py_dict = java_to_py(hm, gw)
print("HashMap ->", py_dict, type(py_dict))

jarr = gw.new_array(gw.jvm.java.lang.String, 3)
jarr[0] = "a"
jarr[1] = "b"
jarr[2] = "c"
py_from_array = java_to_py(jarr, gw)
print("Java array ->", py_from_array)
