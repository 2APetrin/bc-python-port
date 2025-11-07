package benchmarks;

import org.bouncycastle.crypto.digests.SHA256Digest;
import org.openjdk.jmh.annotations.*;

import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeUnit;


@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@State(Scope.Thread)
@Fork(0)
public class Sha256Benchmark {

    @Param({"512", "1024", "2048", "4096", "8192", "16384", "32768", "65536"})
    public int length;  
    private byte[] data;
    private SHA256Digest digest;

    @Setup(Level.Trial)
    public void setup() {
        StringBuilder sb = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
            sb.append((char) ('A' + (i % 26)));
        }
        data = sb.toString().getBytes(StandardCharsets.UTF_8);
        digest = new SHA256Digest();
    }

    @Benchmark
    public byte[] sha256_bouncycastle() {
        digest.reset();
        digest.update(data, 0, data.length);
        byte[] hash = new byte[digest.getDigestSize()];
        digest.doFinal(hash, 0);
        return hash;
    }

    public static void main(String[] args) throws Exception {
        org.openjdk.jmh.Main.main(args);
    }
}
