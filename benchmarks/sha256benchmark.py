from BCPython.BCWrapper import get_gateway
import timeit

lengths = [512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]

make_string = lambda length: ''.join(chr(ord('A') + (i % 26)) for i in range(length)).encode('utf-8')

gw = get_gateway()

digest = gw.jvm.org.bouncycastle.crypto.digests.SHA256Digest()


def sha256_bouncycastle() -> bytes:
    digest.reset()
    digest.update(data, 0, len(data))
    hash = bytes(digest.getDigestSize())
    digest.doFinal(hash, 0)
    return hash


iters = 10000

for i in range(len(lengths)):
    data = make_string(lengths[i])

    for j in range(5):
        timeit.timeit(sha256_bouncycastle, number=iters) # warmup

    time = 0.0
    for k in range(5):
        time += timeit.timeit(sha256_bouncycastle, number=iters)

    print(f"Длина {lengths[i]} Среднее время: {time / (5 * iters):.6f} сек на вызов")
