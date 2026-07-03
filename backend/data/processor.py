import pandas as pd
from datetime import datetime


def clean_news_article(article: dict) -> dict:
    return {
        "title": article.get("title", ""),
        "description": article.get("description", ""),
        "content": article.get("content", article.get("description", "")),
        "source": article.get("source", {}).get("name", "Unknown"),
        "published_at": article.get("publishedAt", datetime.utcnow().isoformat()),
        "url": article.get("url", ""),
    }


def enrich_signal_with_context(signal: dict, brent_price: float, spr_days: float) -> dict:
    signal["context"] = {
        "brent_price": brent_price,
        "spr_days_remaining": spr_days,
        "india_import_dependency": 0.88,
        "hormuz_dependency": 0.43,
    }
    return signal
