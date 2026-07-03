from datetime import datetime
from backend.data.news_ingestion import fetch_news
from backend.data.market_data import get_commodity_prices
from backend.data.processor import clean_news_article, enrich_signal_with_context
from backend.agents.signal_processor import process_articles
from backend.agents.risk_scorer import calculate_risks
from backend.agents.scenario_modeller import model_scenario
from backend.agents.recommender import generate_recommendations


async def run_full_workflow() -> dict:
    signals_data = await fetch_news(page_size=10)
    cleaned = [clean_news_article(a) for a in signals_data]
    signals = await process_articles(cleaned)

    signals_text = " ".join([s.get("title", "") for s in signals_data])
    market_data = await get_commodity_prices()
    brent = float(market_data.get("brent_crude", {}).get("current_price", 95.00))

    enriched_signals = [
        enrich_signal_with_context(s, brent, 9.5) for s in signals
    ]

    risk = await calculate_risks(brent_price=brent, signals=signals_text)

    top_signal = enriched_signals[0] if enriched_signals else {}
    scenario = await model_scenario(
        scenario=f"{top_signal.get('corridor', 'Global')} disruption",
        supply_loss_percent=top_signal.get("probability", 30),
        brent_price=brent,
    )

    supply_gap = int(4800000 * scenario.get("supply_loss_percent", 30) / 100)
    recommendations = await generate_recommendations(
        scenario=scenario.get("scenario_name", "General disruption"),
        supply_gap=supply_gap,
        brent_price=brent,
        confidence=scenario.get("confidence", "medium"),
    )

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "signals": enriched_signals,
        "risk": risk,
        "scenario": scenario,
        "recommendations": recommendations,
    }
