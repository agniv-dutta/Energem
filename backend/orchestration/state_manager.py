import json
from datetime import datetime, timedelta
from typing import Optional

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
