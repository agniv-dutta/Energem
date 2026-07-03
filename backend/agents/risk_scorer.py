import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.config import get_settings

settings = get_settings()

RISK_SCORER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a risk scoring agent for Energem, an energy supply chain resilience system for India.
Calculate disruption risk for India's crude oil corridors.

India imports 88% of crude oil, with 40-45% transiting through the Strait of Hormuz.
Strategic Petroleum Reserves = 9.5 days of national consumption.

Score each scenario on:
- Probability of occurrence (%) in next 30/90 days
- Impact on India's oil availability (% reduction)
- Composite risk (probability × impact / 100) scaled 0-100
- Confidence (high/medium/low)

Corridors to score: Hormuz, Red Sea, Suez, Malacca, Land/Rail Routes

Always output valid JSON only, no markdown formatting."""),
    ("human", """CURRENT CONDITIONS:
- Hormuz flow: {hormuz_flow} bbl/day to India
- Brent price: ${brent_price}/barrel
- SPR reserve: {spr_days} days
- Active signals: {signals}

OUTPUT JSON:
{{
  "corridors": [
    {{
      "corridor": "Hormuz",
      "scenario": "Partial closure (30%)",
      "probability_percent": N,
      "impact_percent": N,
      "composite_risk": N,
      "confidence": "high/medium/low"
    }}
  ],
  "overall_risk_score": N,
  "primary_threat": "...",
  "risk_level": "low/moderate/high/very_high/critical"
}}"""),
])


def _get_llm():
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )


async def calculate_risks(
    hormuz_flow: float = 1500000,
    brent_price: float = 95.00,
    spr_days: float = 9.5,
    signals: str = "No active signals",
) -> dict:
    try:
        llm = _get_llm()
        chain = RISK_SCORER_PROMPT | llm
        response = await chain.ainvoke({
            "hormuz_flow": hormuz_flow,
            "brent_price": brent_price,
            "spr_days": spr_days,
            "signals": signals[:1000],
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
        return _fallback_risk(signals)


def _fallback_risk(signals: str) -> dict:
    risk_level = "moderate"
    overall = 45
    if "houthi" in signals.lower() or "attack" in signals.lower():
        overall = 65
        risk_level = "high"
    elif "hormuz" in signals.lower() or "iran" in signals.lower():
        overall = 55
        risk_level = "high"
    elif "opec" in signals.lower():
        overall = 40
        risk_level = "moderate"

    return {
        "corridors": [
            {
                "corridor": "Hormuz",
                "scenario": "Partial closure (30%)",
                "probability_percent": 35,
                "impact_percent": 30,
                "composite_risk": round(35 * 30 / 100),
                "confidence": "medium",
            },
            {
                "corridor": "Red Sea",
                "scenario": "Shipping disruption",
                "probability_percent": 45,
                "impact_percent": 20,
                "composite_risk": round(45 * 20 / 100),
                "confidence": "medium",
            },
            {
                "corridor": "Suez",
                "scenario": "Political instability",
                "probability_percent": 20,
                "impact_percent": 15,
                "composite_risk": round(20 * 15 / 100),
                "confidence": "low",
            },
            {
                "corridor": "Malacca",
                "scenario": "Piracy or congestion",
                "probability_percent": 15,
                "impact_percent": 10,
                "composite_risk": round(15 * 10 / 100),
                "confidence": "low",
            },
            {
                "corridor": "Land/Rail Routes",
                "scenario": "Sanctions or logistics",
                "probability_percent": 25,
                "impact_percent": 10,
                "composite_risk": round(25 * 10 / 100),
                "confidence": "low",
            },
        ],
        "overall_risk_score": overall,
        "primary_threat": "Houthi attacks on Red Sea shipping escalating to Hormuz disruption",
        "risk_level": risk_level,
    }
