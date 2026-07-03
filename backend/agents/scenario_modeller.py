import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.config import get_settings

settings = get_settings()

SCENARIO_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a scenario modeling agent for Energem, an energy supply chain resilience system for India.
Model the cascading impact of energy supply disruptions on India.

You must calculate and output a timeline of impacts:
- Daily crude shortage (barrels)
- SPR drawdown acceleration
- Days until SPR critical (5-day reserve)
- Refinery run-rate impact
- Domestic fuel price increase
- GDP trajectory impact

Document all assumptions explicitly.

Always output valid JSON only, no markdown formatting."""),
    ("human", """DISRUPTION: {scenario}
DURATION: {duration_days} days
SUPPLY LOSS: {supply_loss_percent}% of current imports
CURRENT BRENT PRICE: ${brent_price}/barrel
SPR RESERVE: {spr_days} days
INDIA DAILY CONSUMPTION: 5.5 million bbl/day
INDIA DAILY IMPORT: 4.8 million bbl/day

OUTPUT JSON:
{{
  "scenario_name": "...",
  "disruption_type": "shipping_reduction",
  "duration_days": N,
  "supply_loss_percent": N,
  "impact_timeline": {{
    "day_1": {{"supply_gap_bbl": N, "spr_drain_days": N, "brent_price": N, "refinery_impact_percent": N}},
    "day_5": {{"supply_gap_bbl": N, "spr_drain_days": N, "brent_price": N, "refinery_impact_percent": N}},
    "day_10": {{"supply_gap_bbl": N, "spr_drain_days": N, "brent_price": N, "refinery_impact_percent": N}},
    "day_30": {{"supply_gap_bbl": N, "spr_drain_days": N, "brent_price": N, "refinery_impact_percent": N}}
  }},
  "price_impact_multiplier": N,
  "gdp_impact_percent": N,
  "assumptions": ["..."],
  "confidence": "high/medium/low"
}}"""),
])


def _get_llm():
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )


async def model_scenario(
    scenario: str = "Hormuz Partial Closure (30%)",
    duration_days: int = 30,
    supply_loss_percent: float = 30,
    brent_price: float = 95.00,
    spr_days: float = 9.5,
) -> dict:
    try:
        llm = _get_llm()
        chain = SCENARIO_PROMPT | llm
        response = await chain.ainvoke({
            "scenario": scenario,
            "duration_days": duration_days,
            "supply_loss_percent": supply_loss_percent,
            "brent_price": brent_price,
            "spr_days": spr_days,
        })
        text = response.content.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        return json.loads(text)
    except Exception:
        return _fallback_scenario(scenario, duration_days, supply_loss_percent, brent_price, spr_days)


def _fallback_scenario(
    scenario: str,
    duration_days: int,
    supply_loss_percent: float,
    brent_price: float,
    spr_days: float,
) -> dict:
    daily_import = 4800000
    daily_gap = int(daily_import * supply_loss_percent / 100)
    price_spike = 1.0 + (supply_loss_percent / 100) * 0.5

    return {
        "scenario_name": scenario,
        "disruption_type": "shipping_reduction",
        "duration_days": duration_days,
        "supply_loss_percent": supply_loss_percent,
        "impact_timeline": {
            "day_1": {
                "supply_gap_bbl": daily_gap,
                "spr_drain_days": round(spr_days - 0.3, 1),
                "brent_price": round(brent_price * 1.08, 2),
                "refinery_impact_percent": -5,
            },
            "day_5": {
                "supply_gap_bbl": daily_gap,
                "spr_drain_days": round(spr_days - 1.5, 1),
                "brent_price": round(brent_price * price_spike, 2),
                "refinery_impact_percent": -12,
            },
            "day_10": {
                "supply_gap_bbl": int(daily_gap * 0.6),
                "spr_drain_days": round(max(spr_days - 3.5, 3.0), 1),
                "brent_price": round(brent_price * max(price_spike - 0.05, 1.0), 2),
                "refinery_impact_percent": -10,
            },
            "day_30": {
                "supply_gap_bbl": int(daily_gap * 0.2),
                "spr_drain_days": round(max(spr_days - 5.0, 2.0), 1),
                "brent_price": round(brent_price * max(price_spike - 0.10, 1.0), 2),
                "refinery_impact_percent": -3,
            },
        },
        "price_impact_multiplier": round(price_spike, 2),
        "gdp_impact_percent": round(-0.3 * (supply_loss_percent / 30), 2),
        "assumptions": [
            "Alternative sourcing takes 10-14 days",
            "SPR drawdown limited to 500K bbl/day max",
            "Demand reduction is slow (inelastic short-term)",
            "Refinery capacity at 250M tonnes/year",
        ],
        "confidence": "medium",
    }
