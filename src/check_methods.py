import subprocess

__all__ = ["ping", "http", "https"]


def ping(location: str, params: dict) -> bool:
    retry_limit = params.get("retry_limit", 1)
    return subprocess.call(
        ["ping", "-c", str(retry_limit), location],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ) == 0


def http(location: str, params: dict, tls=False) -> bool:
    # TODO: implement http
    return True


def https(location: str, params: dict) -> bool:
    return http(location, params, tls=True)
