from urllib.parse import urlparse

def is_valid_url(u: str) -> bool:
    try:
        # only urls with this format get through http(s)://SOMETHING.com(/optional/path)
        p = urlparse(u)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False