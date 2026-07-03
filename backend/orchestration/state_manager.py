import json
from datetime import datetime, timedelta
from typing import Optional
from backend.config import get_settings

settings = get_settings()

try:
    import redis.asyncio as aioredis

    _redis: Optional[aioredis.Redis] = None

    async def get_redis() -> aioredis.Redis:
        global _redis
        if _redis is None:
            _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
        return _redis

    async def cache_set(key: str, value: dict, ttl: int = 300):
        r = await get_redis()
        await r.setex(key, ttl, json.dumps(value))

    async def cache_get(key: str) -> Optional[dict]:
        try:
            r = await get_redis()
            data = await r.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None

except ImportError:

    _store: dict[str, tuple[str, datetime]] = {}

    async def cache_set(key: str, value: dict, ttl: int = 300):
        _store[key] = (json.dumps(value), datetime.utcnow() + timedelta(seconds=ttl))

    async def cache_get(key: str) -> Optional[dict]:
        entry = _store.get(key)
        if not entry:
            return None
        data, expiry = entry
        if datetime.utcnow() > expiry:
            _store.pop(key, None)
            return None
        return json.loads(data)
