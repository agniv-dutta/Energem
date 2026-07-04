import json
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.config import get_settings

settings = get_settings()

ESCALATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a geopolitical analyst for Energem, an energy supply chain resilience system for India.
Analyze a series of news events over the past days to assess the escalation trajectory for energy supply disruption.

Score escalation on a 1-10 scale:
1-3: Routine diplomatic tension, no immediate threat
4-5: Elevated rhetoric, military posturing, plausible escalation
6-7: Active hostilities, economic warfare, crisis imminent
8-10: Open conflict, major supply disruption underway

Always output valid JSON only, no markdown formatting."""),
    ("human", """EVENTS OVER PAST 7 DAYS:
{events}

ANALYZE AND OUTPUT JSON:
{{
  "trajectory": "escalating/de-escalating/stable",
  "trajectory_confidence": "high/medium/low",
  "escalation_score": 1-10,
  "risk_level": "low/moderate/high/critical",
  "critical_trigger": "..." or null,
  "historical_precedent": "...",
  "de_escalation_path": "...",
  "probability_military_action_7_days": N,
  "probability_military_action_14_days": N,
  "probability_military_action_30_days": N,
  "timeline_to_potential_action": "...",
  "affected_corridors": ["Hormuz", "..."],
  "key_actors": ["..."],
  "summary": "..."
}}"""),
])


def _get_llm():
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )


async def assess_escalation(events: list[dict]) -> dict:
    try:
        llm = _get_llm()
        chain = ESCALATION_PROMPT | llm

        events_text = "\n".join(
            f"- [{e.get('publishedAt', e.get('date', 'unknown'))}] {e.get('title', '')}"
            for e in events[-20:]
        )

        response = await chain.ainvoke({"events": events_text})
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
        return _fallback_escalation(events)


def _fallback_escalation(events: list[dict]) -> dict:
    titles = " ".join(e.get("title", "") for e in events).lower()

    score = 3
    trajectory = "stable"
    trigger = None
    corridors = ["global"]
    actors = []

    if "houthi" in titles or "missile" in titles or "attack" in titles:
        score = 7
        trajectory = "escalating"
        trigger = "Houthi missile attack on commercial vessel near Bab al-Mandab"
        corridors = ["red_sea", "hormuz"]
        actors = ["Houthi Movement", "Yemen", "Iran"]
    elif "hormuz" in titles or "iran" in titles or "gulf" in titles:
        score = 6
        trajectory = "escalating"
        trigger = "Iran threatens Hormuz closure or US-Iran military confrontation"
        corridors = ["hormuz"]
        actors = ["Iran", "United States"]
    elif "sanctions" in titles or "ofac" in titles:
        score = 4
        trajectory = "escalating"
        corridors = ["russia_europe", "iran"]
        actors = ["United States", "OFAC"]
    elif "opec" in titles or "production" in titles:
        score = 3
        trajectory = "stable"
        corridors = ["global"]
        actors = ["OPEC+"]

    return {
        "trajectory": trajectory,
        "trajectory_confidence": "medium",
        "escalation_score": score,
        "risk_level": "critical" if score >= 8 else "high" if score >= 6 else "moderate" if score >= 4 else "low",
        "critical_trigger": trigger,
        "historical_precedent": "Similar escalation pattern observed in 2019 Hormuz crisis and 2022 Houthi Red Sea attacks",
        "de_escalation_path": "Diplomatic engagement with regional actors, de-escalation statements, and international maritime security patrols",
        "probability_military_action_7_days": min(score * 5, 70),
        "probability_military_action_14_days": min(score * 8, 85),
        "probability_military_action_30_days": min(score * 10, 95),
        "timeline_to_potential_action": "Immediate" if score >= 7 else "Within 14 days" if score >= 5 else "Unlikely in next 30 days",
        "affected_corridors": corridors,
        "key_actors": actors,
        "summary": f"Escalation score {score}/10 — {trajectory}. Primary threat to {' and '.join(corridors)} corridors.",
    }


async def assess_from_news_api(page_size: int = 20) -> dict:
    from backend.data.news_ingestion import fetch_news
    articles = await fetch_news(query="geopolitical tension energy supply military", page_size=page_size)
    return await assess_escalation(articles)
