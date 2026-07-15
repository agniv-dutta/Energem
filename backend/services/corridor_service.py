from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.db.models import Corridor, Signal, RiskSnapshot, Article
from backend.config import get_settings

settings = get_settings()

SEED_CORRIDORS: list[dict[str, Any]] = [
    {
        "corridor_id": "COR-HORMUZ-01",
        "name": "Strait of Hormuz",
        "key_value": "hormuz",
        "baseline_daily_flow_bbl": 1_500_000,
        "historical_baseline_risk": 78.0,
        "alternative_routes": [
            {"name": "Malacca Strait", "distance_nm": 3100, "transit_days_add": 5, "risk": "viable"},
            {"name": "Suez Canal", "distance_nm": 4800, "transit_days_add": 8, "risk": "moderate"},
        ],
    },
    {
        "corridor_id": "COR-REDSEA-02",
        "name": "Red Sea / Bab al-Mandab",
        "key_value": "red_sea",
        "baseline_daily_flow_bbl": 8_800_000,
        "historical_baseline_risk": 35.0,
        "alternative_routes": [
            {"name": "Cape of Good Hope", "distance_nm": 6200, "transit_days_add": 12, "risk": "viable"},
            {"name": "Suez Canal", "distance_nm": 2400, "transit_days_add": 0, "risk": "same_route"},
        ],
    },
    {
        "corridor_id": "COR-SUEZ-03",
        "name": "Suez Canal",
        "key_value": "suez",
        "baseline_daily_flow_bbl": 5_500_000,
        "historical_baseline_risk": 42.0,
        "alternative_routes": [
            {"name": "Cape of Good Hope", "distance_nm": 6200, "transit_days_add": 14, "risk": "viable"},
            {"name": "SUMED Pipeline", "distance_nm": 200, "transit_days_add": 0, "risk": "viable"},
        ],
    },
    {
        "corridor_id": "COR-MALACCA-04",
        "name": "Strait of Malacca",
        "key_value": "malacca",
        "baseline_daily_flow_bbl": 16_000_000,
        "historical_baseline_risk": 18.0,
        "alternative_routes": [
            {"name": "Lombok Strait", "distance_nm": 1400, "transit_days_add": 3, "risk": "viable"},
            {"name": "Sunda Strait", "distance_nm": 1200, "transit_days_add": 2, "risk": "moderate"},
        ],
    },
    {
        "corridor_id": "COR-LAND-05",
        "name": "Land / Rail Routes",
        "key_value": "land_route",
        "baseline_daily_flow_bbl": 1_200_000,
        "historical_baseline_risk": 25.0,
        "alternative_routes": [
            {"name": "Pipeline (TAPI)", "distance_nm": 1100, "transit_days_add": 0, "risk": "viable"},
        ],
    },
    {
        "corridor_id": "COR-RUS-IND-06",
        "name": "Russia → India (Arctic Route)",
        "key_value": "russia_india",
        "baseline_daily_flow_bbl": 400_000,
        "historical_baseline_risk": 10.0,
        "alternative_routes": [
            {"name": "Black Sea Route", "distance_nm": 5600, "transit_days_add": 6, "risk": "high"},
        ],
    },
]


def seed_corridors(db: Session) -> int:
    existing_ids = {c.corridor_id for c in db.query(Corridor.corridor_id).all()}
    inserted = 0
    for corridor_data in SEED_CORRIDORS:
        if corridor_data["corridor_id"] not in existing_ids:
            db.add(Corridor(**corridor_data))
            inserted += 1
    if inserted:
        db.commit()
    return inserted


def _utcnow() -> datetime:
    return datetime.utcnow()


def _confidence_avg(signals: list[Signal]) -> str:
    if not signals:
        return "low"
    mapping = {"low": 1.0, "medium": 2.0, "high": 3.0}
    avg = sum(mapping.get(s.confidence.lower(), 1.0) for s in signals) / len(signals)
    if avg >= 2.4:
        return "high"
    if avg >= 1.6:
        return "medium"
    return "low"


def _format_iso(dt: datetime | None) -> str:
    if not dt:
        return _utcnow().isoformat() + "Z"
    return dt.isoformat() + "Z"


def _compute_trend(db: Session, corridor_key: str, current_risk: float) -> str:
    now = _utcnow()
    yesterday = now - timedelta(hours=24)
    yesterday_snapshot = (
        db.query(RiskSnapshot)
        .filter(RiskSnapshot.calculated_at <= yesterday)
        .order_by(RiskSnapshot.calculated_at.desc())
        .first()
    )
    if not yesterday_snapshot or not yesterday_snapshot.corridor_scores:
        return "+0 since 24h"
    previous_risk = yesterday_snapshot.corridor_scores.get(corridor_key, 0)
    delta = round(current_risk - previous_risk)
    return f"{delta:+d} since 24h"


def get_dynamic_corridors(db: Session) -> dict[str, Any]:
    corridors = db.query(Corridor).order_by(Corridor.corridor_id).all()
    if not corridors:
        seed_corridors(db)
        corridors = db.query(Corridor).order_by(Corridor.corridor_id).all()

    latest_snapshot = (
        db.query(RiskSnapshot)
        .order_by(RiskSnapshot.calculated_at.desc())
        .first()
    )
    corridor_scores = latest_snapshot.corridor_scores if latest_snapshot else {}

    now = _utcnow()
    active_cutoff = now - timedelta(hours=48)

    result_corridors = []
    for corridor in corridors:
        key = corridor.key_value

        active_signals = (
            db.query(Signal)
            .filter(
                Signal.corridor == key,
                Signal.created_at >= active_cutoff,
            )
            .order_by(Signal.created_at.desc())
            .all()
        )

        risk_score = corridor_scores.get(key, 0.0)
        if risk_score == 0 and active_signals:
            risk_score = round(
                sum(s.probability for s in active_signals) / len(active_signals), 1
            )

        last_signal_at = active_signals[0].created_at if active_signals else None

        flow_disruption_pct = 0.0
        if active_signals:
            disruption_signals = [
                s for s in active_signals
                if s.event_type in ("shipping_block", "attack", "port_closure", "route_blockade")
            ]
            if disruption_signals:
                max_prob = max(s.probability for s in disruption_signals)
                flow_disruption_pct = max_prob

        daily_flow_impacted = int(
            corridor.baseline_daily_flow_bbl * (1 - flow_disruption_pct / 100)
        )

        trend = _compute_trend(db, key, risk_score)

        result_corridors.append({
            "id": corridor.corridor_id,
            "name": corridor.name,
            "key": key,
            "risk_score": round(risk_score, 1),
            "trend": trend,
            "daily_flow_bbl": corridor.baseline_daily_flow_bbl,
            "daily_flow_impacted_bbl": daily_flow_impacted,
            "active_threats": len(active_signals),
            "last_signal": _format_iso(last_signal_at),
            "confidence": _confidence_avg(active_signals),
            "historical_baseline_risk": corridor.historical_baseline_risk,
            "alternative_routes": corridor.alternative_routes or [],
        })

    result_corridors.sort(key=lambda c: c["risk_score"], reverse=True)

    return {
        "corridors": result_corridors,
        "updated_at": _format_iso(now),
        "snapshot_time": _format_iso(latest_snapshot.calculated_at) if latest_snapshot else None,
        "total_active_signals": sum(c["active_threats"] for c in result_corridors),
    }
