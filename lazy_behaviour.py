from py4j.java_gateway import launch_gateway, JavaGateway, GatewayParameters
import threading
import atexit
import time
from pathlib import Path
import secrets
import subprocess


_gateway = None
_lock = threading.Lock()
_script_path = Path(__file__).resolve().parent
_gateway_path = _script_path / "target" / "bc-python-port-1.0-SNAPSHOT-jar-with-dependencies.jar"
_token = secrets.token_urlsafe(48)


def _start_gateway():
    global _gateway_proc

    cmd = [
        "java",
        "-jar", 
        str(_gateway_path),
        _token
    ]

    print(f"[Python][INFO] Starting Java Gateway")
    _gateway_proc = subprocess.Popen(cmd)
    time.sleep(0.5)

    gateway = JavaGateway(
        gateway_parameters=GatewayParameters(auth_token=_token)
    )

    atexit.register(_shutdown_gateway)
    return gateway


def _shutdown_gateway():
    global _gateway_proc, _gateway
    if _gateway is not None:
        try:
            _gateway.shutdown()
        except Exception:
            pass
    if _gateway_proc is not None:
        _gateway_proc.terminate()
        _gateway_proc.wait(timeout=2)
        _gateway_proc = None
    print("[Python][INFO] Gateway stopped")


def get_gateway(timeout_seconds=30):
    global _gateway
    if _gateway is not None:
        return _gateway

    with _lock:
        if _gateway is None:
            _gateway = _start_gateway()
            start = time.time()
            while time.time() - start < timeout_seconds:
                try:
                    _gateway.entry_point  # raise exception if not accessible
                    break
                except Exception:
                    time.sleep(0.1)
            else:
                _gateway.shutdown()
                _gateway = None
                raise RuntimeError("[Python][ERROR] Timed out waiting for Java gateway")
    return _gateway


def main():
    """
    example.py but ran via auto openning gateway
    """
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


if __name__ == "__main__":
    main()
