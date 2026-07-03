import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.config import get_settings

settings = get_settings()

RECOMMENDER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a crude oil procurement strategist for Energem, an energy supply chain resilience system for India.
Given a disruption scenario, recommend adaptive procurement strategies.

Current portfolio: Saudi Arabia 40%, Iraq 20%, Iran 8% (unreliable), Russia 10%, Brazil 5%, Others 17%
SPR reserve: 9.5 days
Budget constraint: None (emergency mode)

For each recommendation provide:
- Implementation timeline (hours/days)
- Volume impact (barrels/day)
- Cost increase ($/barrel premium)
- Geopolitical risk (low/medium/high)
- Confidence (high/medium/low)

Always output valid JSON only, no markdown formatting."""),
    ("human", """DISRUPTION: {scenario}
SUPPLY GAP: {supply_gap} barrels/day
TIME TO ALTERNATE SOURCE: 10-14 days
BRENT PRICE: ${brent_price}/barrel
CONFIDENCE: {confidence}

OUTPUT JSON:
{{
  "scenario": "...",
  "supply_gap_bbl": N,
  "recommendations": [
    {{
      "priority": 1,
      "action": "...",
      "timeline_days": N,
      "volume_bbl": N,
      "cost_premium_dollars_per_barrel": N,
      "geopolitical_risk": "low/medium/high",
      "confidence": "high/medium/low",
      "reasoning": "..."
    }}
  ],
  "composite_strategy": "...",
  "estimated_total_cost_premium": N
}}"""),
])


def _get_llm():
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )


async def generate_recommendations(
    scenario: str = "Hormuz Partial Closure (30%)",
    supply_gap: int = 500000,
    brent_price: float = 95.00,
    confidence: str = "medium",
) -> dict:
    try:
        llm = _get_llm()
        chain = RECOMMENDER_PROMPT | llm
        response = await chain.ainvoke({
            "scenario": scenario,
            "supply_gap": supply_gap,
            "brent_price": brent_price,
            "confidence": confidence,
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
        return _fallback_recommendations(scenario, supply_gap, brent_price)


def _fallback_recommendations(scenario: str, supply_gap: int, brent_price: float) -> dict:
    return {
        "scenario": scenario,
        "supply_gap_bbl": supply_gap,
        "recommendations": [
            {
                "priority": 1,
                "action": f"Increase Russia crude imports by {min(300000, supply_gap)} bbl/day",
                "timeline_days": 12,
                "volume_bbl": min(300000, supply_gap),
                "cost_premium_dollars_per_barrel": 2.50,
                "geopolitical_risk": "medium",
                "confidence": "high",
                "reasoning": "Russia has spare export capacity and political willingness to capitalize on crisis",
            },
            {
                "priority": 2,
                "action": f"Activate spot market for {min(500000, supply_gap)} bbl/day",
                "timeline_days": 3,
                "volume_bbl": min(500000, supply_gap),
                "cost_premium_dollars_per_barrel": 5.00,
                "geopolitical_risk": "low",
                "confidence": "high",
                "reasoning": "Spot market is expensive but provides immediate volume",
            },
            {
                "priority": 3,
                "action": "Accelerate SPR releases to max pumping capacity (500K bbl/day)",
                "timeline_days": 1,
                "volume_bbl": 500000,
                "cost_premium_dollars_per_barrel": 0,
                "geopolitical_risk": "low",
                "confidence": "high",
                "reasoning": "SPR is purpose-built for supply emergencies, no cost premium",
            },
            {
                "priority": 4,
                "action": "Negotiate long-term contracts with Brazil and West Africa",
                "timeline_days": 10,
                "volume_bbl": 200000,
                "cost_premium_dollars_per_barrel": 1.00,
                "geopolitical_risk": "low",
                "confidence": "medium",
                "reasoning": "Diversification reduces future Hormuz dependence",
            },
            {
                "priority": 5,
                "action": "Implement demand-side measures (fuel rationing, coal switching)",
                "timeline_days": 14,
                "volume_bbl": 150000,
                "cost_premium_dollars_per_barrel": 0,
                "geopolitical_risk": "low",
                "confidence": "low",
                "reasoning": "Last resort: politically difficult but buys time",
            },
        ],
        "composite_strategy": "Days 1-5: Spot market + SPR = 1M bbl/day. Days 5-10: Russia arrives. Days 10+: Sustainable alternatives.",
        "estimated_total_cost_premium": 47500000,
    }
