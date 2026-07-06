from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any

import httpx
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.data.news_ingestion import fetch_news
from backend.db.models import Article, RiskSnapshot, Signal
from backend.utils.logging import logger


settings = get_settings()
PENDING_ARTICLE_BUFFER: list[dict[str, Any]] = []


def _utcnow() -> datetime:
    return datetime.utcnow()


def _parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        cleaned = value.replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(cleaned)
        except ValueError:
            return None
        if parsed.tzinfo is not None:
            return parsed.astimezone(tz=None).replace(tzinfo=None)
        return parsed
    return None


def _article_identity(article_data: dict[str, Any]) -> tuple[str, datetime]:
    source = article_data.get("source", {})
    source_name = source.get("name") if isinstance(source, dict) else source
    published_at = _parse_datetime(article_data.get("publishedAt")) or _utcnow()
    return str(source_name or "Unknown"), published_at


def _article_text(article_data: dict[str, Any]) -> tuple[str, str]:
    headline = article_data.get("title") or article_data.get("headline") or "Untitled article"
    description = article_data.get("description") or ""
    content = article_data.get("content") or ""
    body = " ".join(part for part in [description, content] if part).strip() or headline
    return headline, body


def _news_query() -> str:
    return " OR ".join(settings.news_keywords)


def _clamp_score(value: float) -> float:
    return max(0.0, min(100.0, value))


def _signal_id(signal: Signal) -> str:
    return f"SIG-{signal.id:03d}"


def _format_iso_z(value: datetime | None) -> str:
    if not value:
        return _utcnow().isoformat() + "Z"
    return value.isoformat() + "Z"


async def _call_claude(article_text: str) -> dict[str, Any]:
    prompt = f'''
Extract energy supply disruption signals from this news article.

Article: {article_text}

Respond ONLY in JSON:
{{
  "event_type": "attack|sanctions|production_cut|shipping_block|other",
  "corridor": "hormuz|red_sea|malacca|suez|land_route",
  "probability_percent": 0-100,
  "duration_days": estimated_duration,
  "confidence": "high|medium|low",
  "summary": "one sentence",
  "risk_delta": "+/- percent change to composite risk",
  "immediate_action": "increase_sourcing|activate_spr|spot_market|negotiate"
}}
'''.strip()

    if not settings.claude_api_key:
        return _fallback_signal(article_text)

    headers = {
        "x-api-key": settings.claude_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": settings.claude_model,
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}],
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post("https://api.anthropic.com/v1/messages", headers=headers, json=body)
        response.raise_for_status()
        payload = response.json()

    text_chunks: list[str] = []
    for item in payload.get("content", []):
        if isinstance(item, dict) and item.get("type") == "text":
            text_chunks.append(item.get("text", ""))
    extracted_text = "".join(text_chunks).strip()
    if extracted_text.startswith("```json"):
        extracted_text = extracted_text[7:]
    if extracted_text.startswith("```"):
        extracted_text = extracted_text[3:]
    if extracted_text.endswith("```"):
        extracted_text = extracted_text[:-3]
    return json.loads(extracted_text.strip())


def _fallback_signal(article_text: str) -> dict[str, Any]:
    lowered = article_text.lower()
    if any(term in lowered for term in ["houthi", "red sea", "bab al-mandab", "tanker"]):
        return {
            "event_type": "shipping_block",
            "corridor": "red_sea",
            "probability_percent": 72,
            "duration_days": 7,
            "confidence": "medium",
            "summary": "Shipping disruption risk is elevated in the Red Sea corridor.",
            "risk_delta": 18,
            "immediate_action": "increase_sourcing",
        }
    if any(term in lowered for term in ["hormuz", "iran", "strait"]):
        return {
            "event_type": "attack",
            "corridor": "hormuz",
            "probability_percent": 65,
            "duration_days": 10,
            "confidence": "high",
            "summary": "Hormuz disruption risk is rising on geopolitical escalation.",
            "risk_delta": 22,
            "immediate_action": "activate_spr",
        }
    if any(term in lowered for term in ["sanction", "opec", "production cut", "brent"]):
        return {
            "event_type": "sanctions",
            "corridor": "land_route",
            "probability_percent": 48,
            "duration_days": 30,
            "confidence": "medium",
            "summary": "Sanctions or production shifts may tighten crude supply.",
            "risk_delta": 12,
            "immediate_action": "spot_market",
        }
    return {
        "event_type": "other",
        "corridor": "land_route",
        "probability_percent": 30,
        "duration_days": 14,
        "confidence": "low",
        "summary": "General energy disruption signal detected.",
        "risk_delta": 6,
        "immediate_action": "negotiate",
    }


def _load_recent_articles(db: Session) -> list[Article]:
    cutoff = _utcnow() - timedelta(hours=24)
    return (
        db.query(Article)
        .filter(Article.published_at >= cutoff)
        .order_by(Article.published_at.desc(), Article.id.desc())
        .all()
    )


def _load_latest_snapshot(db: Session) -> RiskSnapshot | None:
    return db.query(RiskSnapshot).order_by(RiskSnapshot.calculated_at.desc()).first()


def _snapshot_confidence(active_signals: list[Signal]) -> str:
    if not active_signals:
        return "low"
    score = 0.0
    for signal in active_signals:
        score += {"low": 1.0, "medium": 2.0, "high": 3.0}.get(signal.confidence.lower(), 1.0)
    average = score / len(active_signals)
    if average >= 2.4:
        return "high"
    if average >= 1.6:
        return "medium"
    return "low"


def _active_signals(db: Session) -> list[Signal]:
    now = _utcnow()
    active: list[Signal] = []
    for signal in db.query(Signal).order_by(Signal.created_at.desc()).all():
        published_at = signal.created_at
        article = db.query(Article).filter(Article.id == signal.article_id).first()
        if article and article.published_at:
            published_at = article.published_at
        duration_days = signal.duration_days or 1
        if now <= published_at + timedelta(days=duration_days):
            active.append(signal)
    return active


def _calculate_snapshot(db: Session) -> RiskSnapshot:
    active_signals = _active_signals(db)
    now = _utcnow()
    contributions: list[float] = []
    corridor_buckets: dict[str, list[float]] = {}

    for signal in active_signals:
        article = db.query(Article).filter(Article.id == signal.article_id).first()
        published_at = article.published_at if article and article.published_at else signal.created_at
        age_hours = max((now - published_at).total_seconds() / 3600.0, 0.0)
        recency_multiplier = max(0.25, 1.0 - (age_hours / 24.0) * 0.75)
        impact_weight = settings.corridor_weights.get(signal.corridor.lower(), 1.0)
        contribution = signal.probability * impact_weight * recency_multiplier
        contributions.append(contribution)
        corridor_buckets.setdefault(signal.corridor.lower(), []).append(contribution)

    corridor_scores = {
        corridor: round(sum(values) / len(values), 2)
        for corridor, values in corridor_buckets.items()
    }
    composite_score = round(_clamp_score(sum(contributions) / len(contributions))) if contributions else 0
    snapshot = RiskSnapshot(
        composite_score=composite_score,
        corridor_scores=corridor_scores,
        signals_count=len(active_signals),
        calculated_at=now,
        confidence=_snapshot_confidence(active_signals),
    )
    db.add(snapshot)
    return snapshot


def _queue_article(article_data: dict[str, Any]) -> None:
    PENDING_ARTICLE_BUFFER.append(article_data)


async def flush_pending_articles(db: Session) -> int:
    flushed = 0
    remaining: list[dict[str, Any]] = []
    for article_data in PENDING_ARTICLE_BUFFER:
        try:
            await persist_article_and_signal(db, article_data)
            flushed += 1
        except Exception as exc:
            db.rollback()
            logger.error("Retry of buffered article failed: %s", exc)
            remaining.append(article_data)
    PENDING_ARTICLE_BUFFER[:] = remaining
    return flushed


async def ingest_recent_news(db: Session) -> dict[str, Any]:
    query = _news_query()
    try:
        raw_articles = await fetch_news(query=query, page_size=25)
    except Exception as exc:
        logger.error("NewsAPI failed, falling back to cached articles: %s", exc)
        raw_articles = [
            {
                "title": article.headline,
                "description": article.body,
                "content": article.body,
                "source": {"name": article.source},
                "publishedAt": _format_iso_z(article.published_at),
                "url": article.url,
                "raw": article.raw_json,
            }
            for article in _load_recent_articles(db)
        ]

    cutoff = _utcnow() - timedelta(hours=24)
    recent_articles = []
    for article in raw_articles:
        published_at = _parse_datetime(article.get("publishedAt"))
        if published_at and published_at >= cutoff:
            recent_articles.append(article)

    refreshed_articles = 0
    extracted_signals = 0
    queued_for_retry = 0
    for article_data in recent_articles:
        try:
            result = await persist_article_and_signal(db, article_data)
            refreshed_articles += 1
            extracted_signals += result
        except HTTPException:
            raise
        except Exception as exc:
            db.rollback()
            logger.error("Article processing failed, buffering for retry: %s", exc)
            _queue_article(article_data)
            queued_for_retry += 1

    snapshot = _calculate_snapshot(db)
    return {
        "refreshed_articles": refreshed_articles,
        "extracted_signals": extracted_signals,
        "queued_for_retry": queued_for_retry,
        "snapshot": snapshot,
    }


async def persist_article_and_signal(db: Session, article_data: dict[str, Any]) -> int:
    source_name, published_at = _article_identity(article_data)
    headline, body = _article_text(article_data)
    body_text = body[:4000]
    existing = (
        db.query(Article)
        .filter(Article.source == source_name, Article.published_at == published_at)
        .first()
    )
    if existing:
        article = existing
    else:
        article = Article(
            source=source_name,
            headline=headline,
            body=body_text,
            published_at=published_at,
            raw_json=article_data,
            url=article_data.get("url"),
            extraction_status="pending",
        )
        db.add(article)
        db.flush()

    existing_signal = db.query(Signal).filter(Signal.article_id == article.id).first()
    if existing_signal and article.extraction_status == "extracted":
        return 0

    retry_after = article.retry_after
    if article.extraction_status == "pending_extraction" and retry_after and retry_after > _utcnow():
        return 0

    article_text = f"{headline}\n\n{body_text}".strip()
    try:
        extracted = await _call_claude(article_text)
    except Exception as exc:
        if settings.claude_api_key:
            article.extraction_status = "pending_extraction"
            article.retry_after = _utcnow() + timedelta(minutes=5)
            article.last_error = str(exc)
            db.add(article)
            return 0
        extracted = _fallback_signal(article_text)

    signal = Signal(
        article_id=article.id,
        event_type=str(extracted.get("event_type", "other")),
        corridor=str(extracted.get("corridor", "land_route")),
        probability=float(extracted.get("probability_percent", extracted.get("probability", 0))),
        duration_days=float(extracted.get("duration_days", 1)),
        confidence=str(extracted.get("confidence", "low")),
        extracted_json=extracted,
    )
    article.extraction_status = "extracted"
    article.retry_after = None
    article.last_error = None
    db.add(signal)
    db.add(article)
    db.flush()
    return 1


CATEGORY_EVENT_TYPES: dict[str, list[str] | None] = {
    "all": None,
    "geopolitical": ["sanctions", "war", "embargo", "political_unrest"],
    "maritime": ["shipping_attack", "piracy", "port_closure", "route_blockade"],
    "sanctions": ["sanctions"],
    "market": ["price_spike", "demand_shock", "opec_action"],
}


def _latest_signals(db: Session, limit: int, category: str = "all") -> list[dict[str, Any]]:
    event_types = CATEGORY_EVENT_TYPES.get(category)
    query = (
        db.query(Signal, Article)
        .join(Article, Signal.article_id == Article.id)
        .order_by(Signal.created_at.desc(), Signal.id.desc())
    )
    if event_types is not None:
        query = query.filter(Signal.event_type.in_(event_types))
    rows = query.limit(limit).all()
    items: list[dict[str, Any]] = []
    for signal, article in rows:
        extracted = signal.extracted_json or {}
        classification = []
        if signal.probability >= 70:
            classification.append("critical")
        if signal.confidence == "high":
            classification.append("escalated")
        items.append(
            {
                "id": _signal_id(signal),
                "timestamp": _format_iso_z(signal.created_at),
                "event_type": signal.event_type,
                "headline": article.headline,
                "corridor": signal.corridor,
                "confidence": signal.confidence,
                "classification": classification,
                "body": str(extracted.get("summary", article.body or article.headline)),
                "impact": {
                    "risk_delta": f"{extracted.get('risk_delta', 0):+d}%",
                    "supply_impact": f"{int(signal.probability * 4800)} BBL/DAY",
                    "precedent": str(extracted.get("precedent", "N/A")),
                },
            }
        )
    return items


def _trend_string(db: Session, current_score: float) -> str:
    previous = db.query(RiskSnapshot).order_by(RiskSnapshot.calculated_at.desc()).offset(1).first()
    if not previous:
        return "+0 since yesterday"
    delta = round(current_score - previous.composite_score)
    return f"{delta:+d} since yesterday"


async def refresh_signal_pipeline(db: Session) -> dict[str, Any]:
    await flush_pending_articles(db)
    result = await ingest_recent_news(db)
    snapshot: RiskSnapshot = result["snapshot"]
    db.commit()
    return result | {"trend": _trend_string(db, snapshot.composite_score)}


def get_latest_signal_payload(db: Session, limit: int = 10, category: str = "all") -> dict[str, Any]:
    return {
        "category": category,
        "signals": _latest_signals(db, limit, category),
    }
