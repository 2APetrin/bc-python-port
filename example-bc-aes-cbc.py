from os import urandom
from BCWrapper import get_gateway
from Convertions import java_to_py

gw = get_gateway()
security = gw.jvm.java.security
Security = security.Security
BouncyCastleProvider = gw.jvm.org.bouncycastle.jce.provider.BouncyCastleProvider
Security.addProvider(BouncyCastleProvider())

Cipher = gw.jvm.javax.crypto.Cipher
SecretKeySpec = gw.jvm.javax.crypto.spec.SecretKeySpec
IvParameterSpec = gw.jvm.javax.crypto.spec.IvParameterSpec

key_bytes = urandom(16)   # 128-bit key
iv_bytes = urandom(16)
pt = b"top secret data that needs padding"

key = SecretKeySpec(key_bytes, "AES")
iv = IvParameterSpec(iv_bytes)

cipher = Cipher.getInstance("AES/CBC/PKCS5Padding", "BC")
cipher.init(Cipher.ENCRYPT_MODE, key, iv)
ct = cipher.doFinal(pt)
ct_py = java_to_py(ct, gw)
print("Ciphertext len:", len(ct_py))

cipher2 = Cipher.getInstance("AES/CBC/PKCS5Padding", "BC")
cipher2.init(Cipher.DECRYPT_MODE, key, iv)
pt2 = cipher2.doFinal(ct)
pt2_py = java_to_py(pt2, gw)
print("Decrypted == original:", pt2_py == pt)
