from py4j.java_gateway import JavaGateway, GatewayParameters
from pathlib import Path
from typing import Optional
import threading
import atexit
import time
import secrets
import subprocess


_gateway: Optional[JavaGateway] = None
_lock: threading.Lock = threading.Lock()
_script_path: Path = Path(__file__).resolve().parent
_gateway_path: Path = _script_path / "target" / "bc-python-port-1.0-SNAPSHOT-jar-with-dependencies.jar"
_java_path: Optional[Path] = None
_token: str = secrets.token_urlsafe(48)


def _start_gateway(timeout_seconds) -> JavaGateway:
    global _gateway_proc

    cmd = [
        "java" if _java_path is None else _java_path,
        "-jar",
        str(_gateway_path),
        _token
    ]

    print("[Python][INFO] Starting Java Gateway")
    _gateway_proc = subprocess.Popen(cmd)

    time.sleep(0.5)

    gateway = JavaGateway(
        gateway_parameters=GatewayParameters(auth_token=_token)
    )

    # start = time.time()
    # while time.time() - start < timeout_seconds:
    #     try:
    #         gateway = JavaGateway(
    #             gateway_parameters=GatewayParameters(auth_token=_token)
    #         )
    #     except Exception:
    #         continue
    #     break

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


def get_gateway(timeout_seconds=30) -> JavaGateway:
    global _gateway
    if _gateway is not None:
        return _gateway

    with _lock:
        if _gateway is None:
            _gateway = _start_gateway(timeout_seconds)
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


def set_java_path(pth: str) -> bool:
    """
    returns: False if gateway was already obtained and java_path has not changed
             True  if java_path was set
    """
    global _java_path, _gateway

    if _gateway is not None:
        return False

    path = Path(pth)
    if not path.exists():
        raise FileNotFoundError(f"java_path does not exist: {pth}")
    if not path.is_file():
        raise ValueError(f"java_path does not point to file: {pth}")

    _java_path = Path(pth)
    return True
