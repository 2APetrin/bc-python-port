from BCWrapper import get_gateway
#from BCPython.BCWrapper import get_gateway

gw = get_gateway()

# Получаем доступ к классам Java
Security = gw.jvm.java.security.Security
BouncyCastleProvider = gw.jvm.org.bouncycastle.jce.provider.BouncyCastleProvider

# Создаём экземпляр провайдера
print(BouncyCastleProvider)  # тут ошибка
provider = BouncyCastleProvider()

# Добавляем провайдера в систему безопасности
Security.addProvider(provider)

# Проверяем, что BC добавился как провайдет
for p in gw.jvm.java.security.Security.getProviders():
    print(p.getName())

# Доступаемся к Java штучкам
MessageDigest = gw.jvm.java.security.MessageDigest
Base64 = gw.jvm.java.util.Base64
# Charset = gw.jvm.java.nio.charset.StandardCharsets

text = "hash me please"
text_bytes = text.encode("utf-8")

digest = MessageDigest.getInstance("SHA-256", "BC")
hash_bytes = digest.digest(text_bytes)  # принимает byte[]
encoded = Base64.getEncoder().encodeToString(hash_bytes)
print("SHA-256 (Base64):", encoded)
