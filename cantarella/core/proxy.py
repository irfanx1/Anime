#@cantarellabots
import os
import random

# ── Your hardcoded proxy (always used as fallback) ───────────────────────────
HARDCODED_PROXIES = [
    "http://ucwronij:alp2noubwaah@38.154.185.97:6370",
]

def parse_proxy(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None

    protocol = "http"
    if "://" in line:
        protocol, line = line.split("://", 1)

    if "@" in line:
        return f"{protocol}://{line}"

    parts = line.split(":")
    if len(parts) == 4:
        host, port, user, password = parts
        return f"{protocol}://{user}:{password}@{host}:{port}"
    elif len(parts) == 2:
        host, port = parts
        return f"{protocol}://{host}:{port}"

    return f"{protocol}://{line}"


def load_proxies():
    proxies = []

    # 1. Load from proxies.txt file
    try:
        with open("proxies.txt", "r") as f:
            for line in f:
                proxy = parse_proxy(line)
                if proxy:
                    proxies.append(proxy)
    except FileNotFoundError:
        pass

    # 2. Load from PROXY_LIST env var (comma separated)
    proxy_env = os.environ.get("PROXY_LIST", "")
    if proxy_env:
        for line in proxy_env.replace(",", "\n").splitlines():
            proxy = parse_proxy(line)
            if proxy and proxy not in proxies:
                proxies.append(proxy)

    # 3. Always include hardcoded proxies as fallback
    for proxy in HARDCODED_PROXIES:
        if proxy not in proxies:
            proxies.append(proxy)

    return proxies


_cached_proxies = None

def get_random_proxy():
    global _cached_proxies
    if _cached_proxies is None:
        _cached_proxies = load_proxies()
    if not _cached_proxies:
        return None
    return random.choice(_cached_proxies)

def get_proxy_dict(proxy_url):
    if not proxy_url:
        return None
    if proxy_url.startswith("socks4://") or proxy_url.startswith("socks5://"):
        return {"http": proxy_url, "https": proxy_url}
    return {"http": proxy_url, "https": proxy_url}
