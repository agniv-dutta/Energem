from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from backend.db.models import AuthorizationLog, Recommendation


RISK_ORDER = {"low": 1, "medium": 2, "high": 3}
AUTHORIZATION_LIMITS = {
    "directorate_b": {"max_volume": 1_000_000, "max_risk": "medium"},
    "ministry": {"max_volume": 5_000_000, "max_risk": "high"},
    "emergency": {"max_volume": None, "max_risk": "high"},
}


def _scenario_key_to_int(scenario_id: Optional[str]) -> int:
    if not scenario_id:
        return 1
    digits = "".join(ch for ch in scenario_id if ch.isdigit())
    return int(digits) if digits else 1


def _format_scenario_id(scenario_id: int) -> str:
    return f"SID-{scenario_id:03d}"


def _format_recommendation_id(value: str) -> str:
    if value.startswith("REC-"):
        return value
    return f"REC-{value}"


def _status_detail(recommendation: Recommendation) -> str:
    if recommendation.status == "approved":
        approver = recommendation.approved_by or "system"
        return f"Approved by {approver}"
    if recommendation.status == "pending_execution":
        return "Queued for execution"
    if recommendation.status == "executed":
        return "Execution completed"
    if recommendation.status == "rejected":
        return "Rejected by authority"
    if recommendation.status == "generated":
        return "Generated and awaiting review"
    return "Awaiting directorate B approval"


def _ensure_seeded_recommendations(db: Session, scenario_id: int) -> None:
    existing = db.query(Recommendation).filter(Recommendation.scenario_id == scenario_id).count()
    if existing:
        return

    seeded = [
        Recommendation(
            id="REC-001",
            scenario_id=scenario_id,
            priority=1,
            supplier="Russia",
            volume_bbl_per_day=300_000,
            eta_days=12,
            cost_premium_per_barrel=2.5,
            geopolitical_risk="medium",
            confidence=92,
            reasoning="Russia can redirect existing tanker streams, politically willing",
            status="pending_approval",
            action="Increase Russia crude imports by 300000 bbl/day",
            timeline_days=12,
            volume_bbl=300_000,
        ),
        Recommendation(
            id="REC-002",
            scenario_id=scenario_id,
            priority=2,
            supplier="Spot Market",
            volume_bbl_per_day=250_000,
            eta_days=3,
            cost_premium_per_barrel=3.0,
            geopolitical_risk="low",
            confidence=88,
            reasoning="Spot market provides immediate volume and quick settlement",
            status="pending_approval",
            action="Activate spot market for emergency balancing",
            timeline_days=3,
            volume_bbl=250_000,
        ),
        Recommendation(
            id="REC-003",
            scenario_id=scenario_id,
            priority=3,
            supplier="Brazil",
            volume_bbl_per_day=250_000,
            eta_days=10,
            cost_premium_per_barrel=2.0,
            geopolitical_risk="low",
            confidence=79,
            reasoning="Brazil diversifies away from chokepoints and has spare export capacity",
            status="pending_approval",
            action="Diversify into Brazilian crude contracts",
            timeline_days=10,
            volume_bbl=250_000,
        ),
    ]
    for recommendation in seeded:
        db.add(recommendation)
    db.commit()


def list_procurement_recommendations(
    db: Session,
    scenario_id: Optional[str] = None,
    status: Optional[str] = None,
) -> dict:
    scenario_int = _scenario_key_to_int(scenario_id)
    _ensure_seeded_recommendations(db, scenario_int)

    query = db.query(Recommendation).filter(Recommendation.scenario_id == scenario_int)
    if status:
        query = query.filter(Recommendation.status == status)

    rows = query.order_by(Recommendation.priority.asc()).all()
    all_rows = (
        db.query(Recommendation)
        .filter(Recommendation.scenario_id == scenario_int)
        .order_by(Recommendation.priority.asc())
        .all()
    )

    approved_volume = sum(
        int(row.volume_bbl_per_day or row.volume_bbl or 0)
        for row in all_rows
        if row.status in {"approved", "pending_execution", "executed"}
    )
    blockers = []
    for row in all_rows:
        if row.geopolitical_risk == "high":
            blockers.append(f"REC-{row.priority:03d}: geopolitical_risk exceeds authorization level")
        if row.status in {"generated", "pending_approval"}:
            blockers.append(f"REC-{row.priority:03d}: awaiting approval")

    return {
        "scenario_id": _format_scenario_id(scenario_int),
        "authority_level": "omega",
        "recommendations": [
            {
                "id": row.id,
                "scenario_id": _format_scenario_id(scenario_int),
                "priority": f"{row.priority:02d}",
                "supplier": row.supplier or row.action,
                "volume_bbl_per_day": int(row.volume_bbl_per_day or row.volume_bbl or 0),
                "eta_days": int(row.eta_days or row.timeline_days or 0),
                "cost_premium_per_barrel": float(row.cost_premium_per_barrel or 0),
                "geopolitical_risk": row.geopolitical_risk or "low",
                "confidence": int(row.confidence or 0),
                "reasoning": row.reasoning or "",
                "status": row.status,
                "approved_by": row.approved_by,
                "approved_at": row.approved_at.isoformat() + "Z" if row.approved_at else None,
                "status_detail": _status_detail(row),
            }
            for row in rows
        ],
        "execution_readiness": {
            "total_approved_volume": approved_volume,
            "can_execute_all": bool(all(row.status in {"approved", "pending_execution", "executed"} for row in all_rows) and all_rows),
            "blockers": blockers,
        },
    }


def _risk_allows_authorization(authorization_level: str, total_volume: int, max_risk: str) -> bool:
    limits = AUTHORIZATION_LIMITS[authorization_level]
    if limits["max_volume"] is not None and total_volume >= limits["max_volume"] and authorization_level == "directorate_b":
        return False
    if RISK_ORDER[max_risk] > RISK_ORDER[limits["max_risk"]]:
        return False
    return True


def authorize_recommendations(
    db: Session,
    recommendation_ids: Iterable[str],
    authorized_by: str,
    authorization_level: str,
    reason: str,
) -> dict:
    if authorization_level not in AUTHORIZATION_LIMITS:
        raise ValueError("Invalid authorization level")

    ids = [str(item) for item in recommendation_ids]
    if not ids:
        raise ValueError("No recommendation IDs provided")

    recommendations = (
        db.query(Recommendation)
        .filter(Recommendation.id.in_(ids))
        .order_by(Recommendation.priority.asc())
        .all()
    )

    if len(recommendations) != len(ids):
        raise LookupError("One or more recommendations not found")

    status_set = {recommendation.status for recommendation in recommendations}
    if {"executed", "rejected"} & status_set:
        raise RuntimeError("Recommendation has conflicting status (executed/rejected)")
    if "approved" in status_set:
        raise RuntimeError("Cannot authorize mixed statuses (some already approved)")
    if status_set != {"pending_approval"}:
        raise RuntimeError("Cannot authorize mixed statuses (some already approved)")

    selected_priorities = {recommendation.priority for recommendation in recommendations}
    approved_priorities = {
        recommendation.priority
        for recommendation in db.query(Recommendation)
        .filter(
            Recommendation.scenario_id == recommendations[0].scenario_id,
            Recommendation.status.in_(["approved", "pending_execution", "executed"]),
        )
        .all()
    }
    for recommendation in recommendations:
        for prerequisite_priority in range(1, recommendation.priority):
            if prerequisite_priority not in selected_priorities and prerequisite_priority not in approved_priorities:
                raise RuntimeError("One or more recommendations depend on prior approvals")

    total_volume = int(
        sum(int(recommendation.volume_bbl_per_day or recommendation.volume_bbl or 0) for recommendation in recommendations)
    )
    max_risk_level = max((recommendation.geopolitical_risk or "low" for recommendation in recommendations), key=lambda value: RISK_ORDER.get(value, 1))
    if not _risk_allows_authorization(authorization_level, total_volume, max_risk_level):
        raise PermissionError("Authorization level insufficient for this volume")

    now = datetime.utcnow()
    total_cost = 0.0
    updated = []
    for recommendation in recommendations:
        recommendation.status = "approved"
        recommendation.approved_by = authorized_by
        recommendation.approved_at = now
        total_cost += float(recommendation.volume_bbl_per_day or recommendation.volume_bbl or 0) * float(recommendation.cost_premium_per_barrel or 0)
        db.add(
            AuthorizationLog(
                id=str(uuid4()),
                recommendation_id=recommendation.id,
                action="approved",
                authorized_by=authorized_by,
                reason=reason,
                timestamp=now,
            )
        )
        updated.append(
            {
                "id": recommendation.id,
                "supplier": recommendation.supplier or recommendation.action,
                "status": recommendation.status,
                "approved_at": now.isoformat() + "Z",
            }
        )
        db.add(recommendation)

    db.commit()
    estimated_arrival = max(int(recommendation.eta_days or recommendation.timeline_days or 0) for recommendation in recommendations)
    return {
        "authorized_count": len(recommendations),
        "total_volume_bbl": total_volume,
        "total_cost_premium": f"${int(round(total_cost)):,.0f}",
        "estimated_arrival": f"{estimated_arrival} days",
        "recommendations": updated,
    }
