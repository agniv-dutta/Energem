from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.data.news_ingestion import fetch_news
from backend.data.market_data import get_commodity_prices
from backend.data.sanctions_loader import get_sanctions_summary
from backend.data.processor import clean_news_article, enrich_signal_with_context
from backend.agents.signal_processor import process_articles
from backend.agents.risk_scorer import calculate_risks
from backend.agents.scenario_modeller import model_scenario
from backend.agents.recommender import generate_recommendations
from backend.agents.escalation_detector import assess_escalation
from backend.agents.resilience_scorer import assess_resilience
from backend.agents.geospatial_analyzer import analyze_geospatial
from backend.agents.country_comparator import compare_countries
from backend.agents.simulator import simulate
from backend.db.session import get_db
from backend.db.models import Signal, RiskSnapshot
from backend.services.corridor_service import get_dynamic_corridors
from backend.services.historical_service import get_historical_comparison, seed_historical_events
from backend.services.procurement_workflow import list_procurement_recommendations, authorize_recommendations
from backend.services.news_signals import get_latest_signal_payload, refresh_signal_pipeline
from backend.utils.report_exports import build_overview_pdf, build_procurement_pptx
from backend.api.schemas import (
    NewsQuery,
    ScenarioQuery,
    RecommendQuery,
    SignalResponse,
    LatestSignalsResponse,
    RefreshSignalsResponse,
    RiskResponse,
    ScenarioResponse,
    RecommendationResponse,
    EscalationResponse,
    ResilienceResponse,
    GeospatialResponse,
    CountryComparisonResponse,
    SimulateRequest,
    SimulateResponse,
    DashboardResponse,
    MarketDataResponse,
    ProcurementRecommendationsResponse,
    ProcurementAuthorizeRequest,
    ProcurementAuthorizeResponse,
)

router = APIRouter(prefix="/api", tags=["Energem API"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "app": "Energem", "timestamp": datetime.utcnow().isoformat()}


@router.get("/corridors/status")
async def get_corridor_status(db: Session = Depends(get_db)):
    return get_dynamic_corridors(db)


@router.get("/signals/{signal_id}/historical-comparison")
async def get_historical_comparison_endpoint(signal_id: str, db: Session = Depends(get_db)):
    seed_historical_events(db)
    try:
        numeric_id = int(signal_id.replace("SIG-", "").lstrip("0") or "0")
    except (ValueError, AttributeError):
        raise HTTPException(status_code=400, detail=f"Invalid signal ID format: {signal_id}")
    result = get_historical_comparison(db, numeric_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Signal {signal_id} not found")
    return result


@router.get("/landing")
async def get_landing_data(db: Session = Depends(get_db)):
    latest_snapshot = (
        db.query(RiskSnapshot)
        .order_by(RiskSnapshot.calculated_at.desc())
        .first()
    )
    risk_score = latest_snapshot.composite_score if latest_snapshot else 0
    corridor_scores = latest_snapshot.corridor_scores if latest_snapshot else {}
    top_corridor = max(corridor_scores, key=corridor_scores.get) if corridor_scores else "hormuz"

    signals = (
        db.query(Signal)
        .order_by(Signal.created_at.desc())
        .limit(3)
        .all()
    )
    last_3 = []
    for s in signals:
        extracted = s.extracted_json or {}
        last_3.append({
            "timestamp": s.created_at.strftime("%H:%MZ") if s.created_at else "00:00Z",
            "event": extracted.get("summary", s.event_type.upper()),
            "confidence": s.confidence.upper(),
            "risk_delta": f"+{int(s.probability * 0.2)}%",
        })

    if not last_3:
        last_3 = [
            {"timestamp": "08:42Z", "event": "HORMUZ STRAIT / KINETIC ACTIVITY DETECTED", "confidence": "HIGH", "risk_delta": "+8%"},
            {"timestamp": "09:15Z", "event": "PARADIP TERMINAL / PRESSURE ANOMALY", "confidence": "MEDIUM", "risk_delta": "+2%"},
            {"timestamp": "09:42Z", "event": "MALACCA STRAIT / VESSEL DEVIATION", "confidence": "HIGH", "risk_delta": "+5%"},
        ]

    return {
        "risk_score": risk_score,
        "trend_delta": 18,
        "trend_direction": "up",
        "trend_hours": 24,
        "top_corridor": top_corridor,
        "last_3_signals": last_3,
        "feed_status": "ACTIVE",
        "last_updated_at": latest_snapshot.calculated_at.isoformat() + "Z" if latest_snapshot else datetime.utcnow().isoformat() + "Z",
    }


@router.get("/procurement/export/pptx")
async def export_procurement_pptx(scenario_id: str | None = None, db: Session = Depends(get_db)):
    payload = list_procurement_recommendations(db, scenario_id=scenario_id)
    content = build_procurement_pptx(payload)
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={
            "Content-Disposition": f"attachment; filename=energem_procurement_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pptx"
        },
    )


async def _build_dashboard_payload() -> DashboardResponse:
    signals_data = await fetch_news(page_size=5)
    cleaned = [clean_news_article(a) for a in signals_data]
    signals = await process_articles(cleaned)
    signals_text = " ".join([s.get("title", "") for s in signals_data])

    market_data = await get_commodity_prices()
    brent = float(market_data.get("brent_crude", {}).get("current_price", 95.00))

    risk_result = await calculate_risks(brent_price=brent, signals=signals_text)

    top_signal = signals[0] if signals else {}
    scenario_result = await model_scenario(
        scenario=f"{top_signal.get('corridor', 'Global')} disruption",
        supply_loss_percent=top_signal.get("probability", 30),
        brent_price=brent,
    )

    supply_gap = int(4800000 * scenario_result.get("supply_loss_percent", 30) / 100)
    rec_result = await generate_recommendations(
        scenario=scenario_result.get("scenario_name", "General disruption"),
        supply_gap=supply_gap,
        brent_price=brent,
        confidence=scenario_result.get("confidence", "medium"),
    )

    return DashboardResponse(
        risk=RiskResponse(**risk_result),
        signals=[SignalResponse(**s) for s in signals],
        market_data=MarketDataResponse(**market_data),
        primary_scenario=ScenarioResponse(**scenario_result),
        recommendations=RecommendationResponse(**rec_result),
        timestamp=datetime.utcnow().isoformat(),
    )


@router.get("/dashboard/export/pdf")
async def export_dashboard_pdf():
    payload = await _build_dashboard_payload()
    content = build_overview_pdf(payload.model_dump())
    return StreamingResponse(
        iter([content]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=energem_overview_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
        },
    )


@router.post("/news")
async def get_news(query: NewsQuery):
    articles = await fetch_news(query=query.query, page_size=query.page_size)
    return {"articles": [clean_news_article(a) for a in articles], "count": len(articles)}


@router.post("/signals")
async def extract_signals(query: NewsQuery) -> list[SignalResponse]:
    articles = await fetch_news(query=query.query, page_size=query.page_size)
    cleaned = [clean_news_article(a) for a in articles]
    signals = await process_articles(cleaned)
    return [SignalResponse(**s) for s in signals]


@router.get("/procurement/recommendations", response_model=ProcurementRecommendationsResponse)
async def get_procurement_recommendations(
    scenario_id: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    payload = list_procurement_recommendations(db, scenario_id=scenario_id, status=status)
    return ProcurementRecommendationsResponse(**payload)


@router.post("/procurement/authorize", response_model=ProcurementAuthorizeResponse)
async def authorize_procurement(request: ProcurementAuthorizeRequest, db: Session = Depends(get_db)):
    try:
        payload = authorize_recommendations(
            db=db,
            recommendation_ids=request.recommendation_ids,
            authorized_by=request.authorized_by,
            authorization_level=request.authorization_level,
            reason=request.reason,
        )
        return ProcurementAuthorizeResponse(**payload)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        message = str(exc)
        if "conflicting status" in message:
            raise HTTPException(status_code=409, detail=message) from exc
        if "depends on prior approvals" in message:
            raise HTTPException(status_code=424, detail=message) from exc
        raise HTTPException(status_code=400, detail=message) from exc


@router.get("/signals/latest", response_model=LatestSignalsResponse)
async def latest_signals(
    category: str = Query("all", alias="category"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    payload = get_latest_signal_payload(db, limit=limit, category=category)
    if payload["signals"]:
        return LatestSignalsResponse(**payload)

    await refresh_signal_pipeline(db)
    latest = get_latest_signal_payload(db, limit=limit, category=category)
    return LatestSignalsResponse(**latest)


@router.post("/signals/refresh", response_model=RefreshSignalsResponse)
async def refresh_signals(db: Session = Depends(get_db)):
    result = await refresh_signal_pipeline(db)
    snapshot = result["snapshot"]
    return RefreshSignalsResponse(
        refreshed_articles=result["refreshed_articles"],
        extracted_signals=result["extracted_signals"],
        current_risk_score=int(round(snapshot.composite_score)),
        confidence=snapshot.confidence,
        queued_for_retry=result.get("queued_for_retry", 0),
    )


@router.get("/risk")
async def get_risk() -> RiskResponse:
    signals_data = await fetch_news(page_size=5)
    signals_text = " ".join([s.get("title", "") for s in signals_data])
    market_data = await get_commodity_prices()
    brent = market_data.get("brent_crude", {}).get("current_price", 95.00)
    result = await calculate_risks(brent_price=float(brent), signals=signals_text)
    return RiskResponse(**result)


@router.post("/scenario")
async def get_scenario(query: ScenarioQuery) -> ScenarioResponse:
    result = await model_scenario(
        scenario=query.scenario,
        duration_days=query.duration_days,
        supply_loss_percent=query.supply_loss_percent,
        brent_price=query.brent_price,
        spr_days=query.spr_days,
    )
    return ScenarioResponse(**result)


@router.post("/recommend")
async def get_recommendations(query: RecommendQuery) -> RecommendationResponse:
    result = await generate_recommendations(
        scenario=query.scenario,
        supply_gap=query.supply_gap,
        brent_price=query.brent_price,
        confidence=query.confidence,
    )
    return RecommendationResponse(**result)


@router.get("/market")
async def get_market() -> MarketDataResponse:
    data = await get_commodity_prices()
    return MarketDataResponse(**data)


@router.get("/sanctions")
async def get_sanctions():
    return await get_sanctions_summary()


@router.get("/escalation")
async def get_escalation() -> EscalationResponse:
    from backend.data.news_ingestion import fetch_news
    articles = await fetch_news(query="geopolitical tension military conflict energy", page_size=15)
    result = await assess_escalation(articles)
    return EscalationResponse(**result)


@router.post("/escalation/assess")
async def assess_events(query: NewsQuery) -> EscalationResponse:
    articles = await fetch_news(query=query.query, page_size=query.page_size)
    result = await assess_escalation(articles)
    return EscalationResponse(**result)


@router.get("/resilience")
async def get_resilience() -> ResilienceResponse:
    signals_data = await fetch_news(page_size=5)
    signals_text = " ".join([s.get("title", "") for s in signals_data])
    scenario_details = "Current geopolitical situation affecting India's crude oil supply chain"
    result = await assess_resilience(scenario_details=scenario_details, signals=signals_text)
    return ResilienceResponse(**result)


@router.post("/resilience/assess")
async def assess_resilience_endpoint(query: ScenarioQuery) -> ResilienceResponse:
    signals_data = await fetch_news(page_size=5)
    signals_text = " ".join([s.get("title", "") for s in signals_data])
    scenario_details = f"Scenario: {query.scenario}, Duration: {query.duration_days}d, Supply loss: {query.supply_loss_percent}%"
    result = await assess_resilience(scenario_details=scenario_details, signals=signals_text)
    return ResilienceResponse(**result)


@router.get("/geospatial")
async def get_geospatial() -> GeospatialResponse:
    signals_data = await fetch_news(page_size=5)
    signals_text = " ".join([s.get("title", "") for s in signals_data])
    risk_result = await calculate_risks(
        brent_price=95.00,
        signals=signals_text,
    )
    result = await analyze_geospatial(risk_scores=risk_result.get("corridors", []))
    return GeospatialResponse(**result)


@router.get("/compare")
async def get_comparison() -> CountryComparisonResponse:
    signals_data = await fetch_news(page_size=5)
    context = " ".join([s.get("title", "") for s in signals_data])
    result = await compare_countries(context=context)
    return CountryComparisonResponse(**result)


@router.post("/scenarios/simulate", response_model=SimulateResponse)
async def run_simulation(req: SimulateRequest):
    result = simulate(
        corridor=req.corridor,
        disruption_percent=req.disruption_percent,
        duration_days=req.duration_days,
        affected_nodes=req.affected_nodes,
        scenario_name=req.scenario_name,
        alternatives_activated=req.alternatives_activated,
    )
    return result


@router.get("/dashboard")
async def get_dashboard() -> DashboardResponse:
    signals_data = await fetch_news(page_size=5)
    cleaned = [clean_news_article(a) for a in signals_data]
    signals = await process_articles(cleaned)
    signals_text = " ".join([s.get("title", "") for s in signals_data])

    market_data = await get_commodity_prices()
    brent = float(market_data.get("brent_crude", {}).get("current_price", 95.00))

    risk_result = await calculate_risks(brent_price=brent, signals=signals_text)

    top_signal = signals[0] if signals else {}
    scenario_result = await model_scenario(
        scenario=f"{top_signal.get('corridor', 'Global')} disruption",
        supply_loss_percent=top_signal.get("probability", 30),
        brent_price=brent,
    )

    supply_gap = int(4800000 * scenario_result.get("supply_loss_percent", 30) / 100)
    rec_result = await generate_recommendations(
        scenario=scenario_result.get("scenario_name", "General disruption"),
        supply_gap=supply_gap,
        brent_price=brent,
        confidence=scenario_result.get("confidence", "medium"),
    )

    return DashboardResponse(
        risk=RiskResponse(**risk_result),
        signals=[SignalResponse(**s) for s in signals],
        market_data=MarketDataResponse(**market_data),
        primary_scenario=ScenarioResponse(**scenario_result),
        recommendations=RecommendationResponse(**rec_result),
        timestamp=datetime.utcnow().isoformat(),
    )
