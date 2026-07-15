from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from backend.db.models import HistoricalEvent, Signal


SEED_HISTORICAL_EVENTS: list[dict[str, Any]] = [
    {
        "event_name": "2022 Yemen Houthi Attacks",
        "event_date": datetime(2022, 10, 12),
        "corridor_affected": "red_sea",
        "duration_days": 8,
        "disruption_percent": 35.0,
        "price_impact_percent": 12.5,
        "supply_loss_bbl": 500_000,
        "lessons_learned": "Attacks lasted 8 days, Brent jumped 12.5%, demonstrated Red Sea vulnerability. India diverted 2 tankers via Cape of Good Hope at +$1.50/bbl premium.",
    },
    {
        "event_name": "2019 Hormuz Tanker Incident",
        "event_date": datetime(2019, 6, 13),
        "corridor_affected": "hormuz",
        "duration_days": 3,
        "disruption_percent": 15.0,
        "price_impact_percent": 8.0,
        "supply_loss_bbl": 300_000,
        "lessons_learned": "Brief but sharp spike, recovered quickly as tensions de-escalated. Demonstrates Hormuz sensitivity to IRGCN activity.",
    },
    {
        "event_name": "2020 Saudi Aramco Drone Strikes",
        "event_date": datetime(2020, 9, 14),
        "corridor_affected": "hormuz",
        "duration_days": 14,
        "disruption_percent": 50.0,
        "price_impact_percent": 20.0,
        "supply_loss_bbl": 1_000_000,
        "lessons_learned": "Drone strikes cut production by 50%. Recovery took 2 weeks. India activated SPR drawdown of 3 days.",
    },
    {
        "event_name": "1973 OPEC Oil Embargo",
        "event_date": datetime(1973, 10, 16),
        "corridor_affected": "hormuz",
        "duration_days": 120,
        "disruption_percent": 75.0,
        "price_impact_percent": 400.0,
        "supply_loss_bbl": 2_500_000,
        "lessons_learned": "Long-term embargo with extreme price impact. Demonstrated complete supply chain fragility. Led to modern SPR programs.",
    },
    {
        "event_name": "2023 Red Sea Houthi Campaign",
        "event_date": datetime(2023, 11, 19),
        "corridor_affected": "red_sea",
        "duration_days": 90,
        "disruption_percent": 45.0,
        "price_impact_percent": 15.0,
        "supply_loss_bbl": 2_000_000,
        "lessons_learned": "Sustained campaign forced major shipping reroutes via Cape of Good Hope. Added 10-14 days transit. Insurance premiums doubled.",
    },
]


def seed_historical_events(db: Session) -> int:
    existing = db.query(HistoricalEvent).count()
    if existing:
        return 0
    for event_data in SEED_HISTORICAL_EVENTS:
        db.add(HistoricalEvent(**event_data))
    db.commit()
    return len(SEED_HISTORICAL_EVENTS)


def _calculate_similarity(
    curr_prob: float,
    curr_duration: float | None,
    hist_prob: float,
    hist_duration: int,
) -> float:
    prob_diff = abs(curr_prob - hist_prob) / 100.0
    dur_diff = abs((curr_duration or 15) - hist_duration) / max(hist_duration, 30)
    similarity = 100 - ((prob_diff * 0.6 + dur_diff * 0.4) * 100)
    return round(max(0, similarity), 1)


def get_historical_comparison(db: Session, signal_id: str) -> dict[str, Any] | None:
    signal = db.query(Signal).filter(Signal.id == signal_id).first()
    if not signal:
        return None

    corridor = signal.corridor
    probability = signal.probability
    duration = signal.duration_days

    events = (
        db.query(HistoricalEvent)
        .filter(HistoricalEvent.corridor_affected == corridor)
        .order_by(HistoricalEvent.event_date.desc())
        .all()
    )

    if not events:
        events = (
            db.query(HistoricalEvent)
            .order_by(HistoricalEvent.event_date.desc())
            .limit(3)
            .all()
        )

    comparisons = []
    now = datetime.utcnow()
    for event in events:
        similarity = _calculate_similarity(probability, duration, event.disruption_percent, event.duration_days)
        years_ago = (now - event.event_date).days // 365

        comparisons.append({
            "historical_event": event.event_name,
            "date": event.event_date.isoformat(),
            "years_ago": years_ago,
            "similarity_score": similarity,
            "comparison": {
                "current_event": {
                    "probability": probability,
                    "estimated_duration": duration or 15,
                },
                "historical_event": {
                    "actual_disruption": event.disruption_percent,
                    "actual_duration": event.duration_days,
                    "actual_supply_loss": event.supply_loss_bbl,
                },
                "delta": {
                    "duration_diff": (duration or event.duration_days) - event.duration_days,
                    "severity_diff": round(probability - event.disruption_percent, 1),
                    "price_impact_historical": event.price_impact_percent,
                },
            },
            "lessons_learned": event.lessons_learned,
        })

    comparisons.sort(key=lambda c: c["similarity_score"], reverse=True)

    best = comparisons[0] if comparisons else None
    recommendation = (
        f"Most similar to {best['historical_event']} ({best['years_ago']} years ago). "
        f"Lesson: {best['lessons_learned']}"
        if best
        else "Insufficient historical data for comparison."
    )

    return {
        "signal_id": f"SIG-{signal.id:03d}",
        "current_signal": {
            "summary": signal.extracted_json.get("summary", "") if signal.extracted_json else "",
            "corridor": corridor,
            "probability": probability,
            "estimated_duration": duration,
            "detected_at": signal.created_at.isoformat() + "Z" if signal.created_at else None,
        },
        "historical_comparisons": comparisons,
        "recommendation": recommendation,
    }
