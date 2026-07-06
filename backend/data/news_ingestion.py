from datetime import datetime, timedelta, timezone

import httpx
from typing import Optional
from backend.config import get_settings

settings = get_settings()


async def fetch_news(query: str = "energy supply disruption oil", page_size: int = 10) -> list[dict]:
    if not settings.newsapi_key:
        return _get_mock_news(query)

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": settings.newsapi_key,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("articles", [])


def _get_mock_news(query: str) -> list[dict]:
    now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    return [
        {
            "title": "Houthi forces fire missile at oil tanker near Bab al-Mandab Strait",
            "description": "A missile attack targeted an oil tanker near the strategic Bab al-Mandab strait, raising concerns about energy supply disruptions through the Red Sea corridor.",
            "content": "Yemen's Houthi forces claimed responsibility for a missile attack on an oil tanker near the Bab al-Mandab strait...",
            "source": {"name": "Reuters"},
            "publishedAt": (now - timedelta(hours=2)).isoformat().replace("+00:00", "Z"),
            "url": "https://reuters.com/article/houthi-attack-oil-tanker",
        },
        {
            "title": "Brent crude jumps 8% as US-Iran tensions escalate",
            "description": "Oil prices surged after Iran threatened to block the Strait of Hormuz in response to increased US military presence in the Gulf.",
            "content": "Brent crude futures rose 8% to $102.50 per barrel on Tuesday after Iran's Revolutionary Guard...",
            "source": {"name": "Bloomberg"},
            "publishedAt": (now - timedelta(hours=4)).isoformat().replace("+00:00", "Z"),
            "url": "https://bloomberg.com/article/brent-crude-iran-tensions",
        },
        {
            "title": "OPEC+ considers emergency meeting amid falling global demand",
            "description": "OPEC and its allies are considering an emergency meeting to address declining global oil demand and potential supply surplus.",
            "content": "OPEC+ delegates indicated that a emergency meeting could be called within weeks...",
            "source": {"name": "Financial Times"},
            "publishedAt": (now - timedelta(hours=6)).isoformat().replace("+00:00", "Z"),
            "url": "https://ft.com/article/opec-emergency-meeting",
        },
    ]
