from BCPython.BCWrapper import get_gateway
import timeit
import random


key_sizes = [1024, 2048, 3072, 4096]

gw = get_gateway()

RSAKeyPairGenerator = gw.jvm.org.bouncycastle.crypto.generators.RSAKeyPairGenerator
RSAKeyGenerationParameters = gw.jvm.org.bouncycastle.crypto.params.RSAKeyGenerationParameters
SecureRandom = gw.jvm.java.security.SecureRandom
RSAEngine = gw.jvm.org.bouncycastle.crypto.engines.RSAEngine
BigInteger = gw.jvm.java.math.BigInteger
Arrays = gw.jvm.java.util.Arrays

iters = 1000

for key_size in key_sizes:
    print(f"\n=== Тестирование RSA {key_size} бит ===")
    
    # RSA key gen
    generator = RSAKeyPairGenerator()
    generator.init(RSAKeyGenerationParameters(
        BigInteger("65537"),
        SecureRandom(),
        key_size,
        100  # certainty
    ))
    
    keyPair = generator.generateKeyPair()
    publicKey = keyPair.getPublic()
    privateKey = keyPair.getPrivate()
    
    # init engines
    encrypt_engine = RSAEngine()
    decrypt_engine = RSAEngine()
    
    # preparation of test data
    max_data_size = (key_size // 8) - 11
    test_data_size = min(32, max_data_size)
    
    # test data as Python bytes
    java_test_data = bytes([random.randint(0, 255) for _ in range(test_data_size)])
    
    
    print(f"Тест шифрования (данные: {test_data_size} байт):")
    
    def rsa_encrypt():
        encrypt_engine.init(True, publicKey)
        return encrypt_engine.processBlock(java_test_data, 0, len(java_test_data))
    
    for _ in range(3):
        timeit.timeit(rsa_encrypt, number=100)
    
    encrypt_times = []
    for _ in range(5):
        time_taken = timeit.timeit(rsa_encrypt, number=iters)
        encrypt_times.append(time_taken / iters)
    
    avg_encrypt = sum(encrypt_times) / len(encrypt_times)
    print(f"  Среднее время: {avg_encrypt * 1_000_000:.2f} мкс на операцию")
    
    encrypt_engine.init(True, publicKey)
    encrypted_data = encrypt_engine.processBlock(java_test_data, 0, len(java_test_data))
    

    print(f"Тест расшифрования:")
    
    def rsa_decrypt():
        decrypt_engine.init(False, privateKey)
        return decrypt_engine.processBlock(encrypted_data, 0, len(encrypted_data))
    
    for _ in range(3):
        timeit.timeit(rsa_decrypt, number=100)
    
    decrypt_times = []
    for _ in range(5):
        time_taken = timeit.timeit(rsa_decrypt, number=iters)
        decrypt_times.append(time_taken / iters)
    
    avg_decrypt = sum(decrypt_times) / len(decrypt_times)
    print(f"  Среднее время: {avg_decrypt * 1_000_000:.2f} мкс на операцию")
    

    print(f"Тест полного цикла (шифрование + расшифрование):")
    
    def rsa_full_cycle():
        encrypt_engine.init(True, publicKey)
        encrypted = encrypt_engine.processBlock(java_test_data, 0, len(java_test_data))
        
        decrypt_engine.init(False, privateKey)
        return decrypt_engine.processBlock(encrypted, 0, len(encrypted))
    
    for _ in range(3):
        timeit.timeit(rsa_full_cycle, number=50)
    
    cycle_times = []
    for _ in range(5):
        time_taken = timeit.timeit(rsa_full_cycle, number=iters // 2)
        cycle_times.append(time_taken / (iters // 2))
    
    avg_cycle = sum(cycle_times) / len(cycle_times)
    print(f"  Среднее время: {avg_cycle * 1_000_000:.2f} мкс на цикл")
