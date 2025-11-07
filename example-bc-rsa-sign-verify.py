from BCWrapper import get_gateway

gw = get_gateway()
security = gw.jvm.java.security
Security = security.Security
BouncyCastleProvider = gw.jvm.org.bouncycastle.jce.provider.BouncyCastleProvider
Security.addProvider(BouncyCastleProvider())

KeyPairGenerator = security.KeyPairGenerator
kpg = KeyPairGenerator.getInstance("RSA", "BC")
kpg.initialize(2048)  # bits
kp = kpg.generateKeyPair()
priv = kp.getPrivate()
pub = kp.getPublic()

data = b"important message"

Signature = security.Signature
signer = Signature.getInstance("SHA256withRSA", "BC")
signer.initSign(priv)
signer.update(data)
sig = signer.sign()

print("Signature (len):", len(sig))

verifier = Signature.getInstance("SHA256withRSA", "BC")
verifier.initVerify(pub)
verifier.update(data)
ok = verifier.verify(sig)
print("Signature ok:", ok)
