package benchmarks;

import org.bouncycastle.crypto.AsymmetricCipherKeyPair;
import org.bouncycastle.crypto.engines.RSAEngine;
import org.bouncycastle.crypto.generators.RSAKeyPairGenerator;
import org.bouncycastle.crypto.params.*;
import org.openjdk.jmh.annotations.*;

import java.security.SecureRandom;
import java.util.concurrent.TimeUnit;
import java.math.BigInteger;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@State(Scope.Thread)
@Fork(0)
public class RSABenchmark {

    @Param({"1024", "2048", "3072", "4096"})
    public int keySize;
    
    private AsymmetricCipherKeyPair keyPair;
    private RSAEngine encryptEngine;
    private RSAEngine decryptEngine;
    private byte[] testData;
    private byte[] encryptedData;

    @Setup(Level.Trial)
    public void setup() {
        // generation of RSA keys
        RSAKeyPairGenerator generator = new RSAKeyPairGenerator();
        generator.init(new RSAKeyGenerationParameters(
            BigInteger.valueOf(65537),
            new SecureRandom(),
            keySize,
            100 // certainty
        ));
        
        keyPair = generator.generateKeyPair();
        
        // init engines
        encryptEngine = new RSAEngine();
        encryptEngine.init(true, keyPair.getPublic());
        
        decryptEngine = new RSAEngine();
        decryptEngine.init(false, keyPair.getPrivate());
        
        // preparation of test data
        int maxDataSize = (keySize / 8) - 11; // for PKCS#1 v1.5 padding
        testData = new byte[Math.min(32, maxDataSize)]; // 32 bytes or less
        new SecureRandom().nextBytes(testData);
        
        // pre-encryption of data for decryption tests
        encryptedData = encryptEngine.processBlock(testData, 0, testData.length);
    }

    @Benchmark
    public byte[] rsa_encrypt() {
        encryptEngine.init(true, keyPair.getPublic());
        return encryptEngine.processBlock(testData, 0, testData.length);
    }

    @Benchmark
    public byte[] rsa_decrypt() {
        decryptEngine.init(false, keyPair.getPrivate());
        return decryptEngine.processBlock(encryptedData, 0, encryptedData.length);
    }

    @Benchmark
    public byte[] rsa_full_cycle() {
        encryptEngine.init(true, keyPair.getPublic());
        byte[] encrypted = encryptEngine.processBlock(testData, 0, testData.length);
        
        decryptEngine.init(false, keyPair.getPrivate());
        return decryptEngine.processBlock(encrypted, 0, encrypted.length);
    }

    public static void main(String[] args) throws Exception {
        org.openjdk.jmh.Main.main(args);
    }
}