from py4j.java_gateway import JavaGateway

gateway = JavaGateway()

# Получаем доступ к классам Java
Security = gateway.jvm.java.security.Security
BouncyCastleProvider = gateway.jvm.org.bouncycastle.jce.provider.BouncyCastleProvider

# Создаём экземпляр провайдера
provider = BouncyCastleProvider()

# Добавляем провайдера в систему безопасности
Security.addProvider(provider)

# Проверяем, что BC добавился как провайдет
for p in gateway.jvm.java.security.Security.getProviders():
    print(p.getName())

# Доступаемся к Java штучкам
MessageDigest = gateway.jvm.java.security.MessageDigest
Base64 = gateway.jvm.java.util.Base64
Charset = gateway.jvm.java.nio.charset.StandardCharsets


text = "hash me please"
text_bytes = text.encode("utf-8")

digest = MessageDigest.getInstance("SHA-256", "BC")
hash_bytes = digest.digest(text_bytes)  # принимает byte[]
encoded = Base64.getEncoder().encodeToString(hash_bytes)
print("SHA-256 (Base64):", encoded)

gateway.shutdown()
