from BCPython.BCWrapper import get_gateway

gw = get_gateway()
security = gw.jvm.java.security
Security = security.Security
BouncyCastleProvider = gw.jvm.org.bouncycastle.jce.provider.BouncyCastleProvider
Security.addProvider(BouncyCastleProvider())

text = "hash me please".encode("utf-8")

MessageDigest = security.MessageDigest
digest = MessageDigest.getInstance("SHA-256", "BC")
hash_bytes = digest.digest(text)               # java byte[] -> py bytes (через py4j)
print("SHA-256 (hex):", hash_bytes.hex())
