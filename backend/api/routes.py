from datetime import datetime
from fastapi import APIRouter, HTTPException
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
from backend.api.schemas import (
    NewsQuery,
    ScenarioQuery,
    RecommendQuery,
    SignalResponse,
    RiskResponse,
    ScenarioResponse,
    RecommendationResponse,
    EscalationResponse,
    ResilienceResponse,
    GeospatialResponse,
    CountryComparisonResponse,
    DashboardResponse,
    MarketDataResponse,
)

router = APIRouter(prefix="/api", tags=["Energem API"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "app": "Energem", "timestamp": datetime.utcnow().isoformat()}


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
