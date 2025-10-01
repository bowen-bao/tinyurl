# backend/shortener/services.py
from django.db import transaction
from .models import Link
from .base62 import encode
import redis
from decouple import config

r = redis.Redis.from_url(config("REDIS_URL"))

def get_cached_url(code):
    url = r.get(code)
    return url.decode() if url else None

def cache_url(code, long_url, ttl=3600):
    r.setex(code, ttl, long_url)

@transaction.atomic
def create_short_link(long_url: str, custom_code: str | None = None) -> Link:
    if custom_code:
        # allow custom aliases if they’re free
        if Link.objects.filter(code=custom_code).exists():
            raise ValueError("Code already taken")
        return Link.objects.create(code=custom_code, long_url=long_url)

    # provisional row to get an ID
    temp = Link.objects.create(code="tmp", long_url=long_url)
    code = encode(temp.id)
    temp.code = code
    temp.save(update_fields=["code"])
    return temp



