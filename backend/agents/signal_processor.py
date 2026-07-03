import json
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.config import get_settings

settings = get_settings()

SIGNAL_EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a geopolitical signal extraction agent for Energem, an energy supply chain resilience system for India.
Analyze news articles for energy supply disruption signals.

Identify:
1. What disruption event is described? (e.g., Houthi attack, sanctions, war)
2. Which corridor is affected? (Hormuz, Red Sea, Suez, Malacca, Russia-Europe)
3. What is the disruption probability? (0-100)
4. What is the likely duration in days?
5. Historical precedent? (e.g., "Similar to 2022 Yemen attacks")
6. Confidence in interpretation? (high/medium/low)

Always output valid JSON only, no markdown formatting."""),
    ("human", """ARTICLE TITLE: {title}
ARTICLE DESCRIPTION: {description}
ARTICLE CONTENT: {content}
SOURCE: {source}
PUBLISHED: {published_at}

OUTPUT JSON:
{{
  "event": "...",
  "corridor": "...",
  "probability": 0-100,
  "duration_days": N,
  "precedent": "...",
  "confidence": "high/medium/low",
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


async def extract_signal(
    title: str,
    description: str,
    content: str,
    source: str = "Unknown",
    published_at: str = "",
) -> dict:
    try:
        llm = _get_llm()
        chain = SIGNAL_EXTRACTION_PROMPT | llm
        response = await chain.ainvoke({
            "title": title,
            "description": description,
            "content": content[:2000],
            "source": source,
            "published_at": published_at,
        })
        text = response.content.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        result = json.loads(text)
        result["source"] = source
        return result
    except Exception:
        return _fallback_signal(title, description)


def _fallback_signal(title: str, description: str) -> dict:
    title_lower = (title + " " + description).lower()
    if "houthi" in title_lower or "red sea" in title_lower or "bab" in title_lower:
        return {
            "event": "houthi_attack",
            "corridor": "red_sea",
            "probability": 65,
            "duration_days": 7,
            "precedent": "Similar to 2022-2024 Houthi Red Sea attacks",
            "confidence": "medium",
            "summary": "Houthi attack on Red Sea shipping threatens alternative Suez route for Indian crude imports",
            "source": "",
        }
    if "hormuz" in title_lower or "iran" in title_lower or "gulf" in title_lower:
        return {
            "event": "geopolitical_tension",
            "corridor": "hormuz",
            "probability": 40,
            "duration_days": 14,
            "precedent": "Similar to 2019 US-Iran tanker crisis",
            "confidence": "medium",
            "summary": "Geopolitical tension in Gulf region threatens Hormuz Strait chokepoint",
            "source": "",
        }
    if "opec" in title_lower or "production cut" in title_lower:
        return {
            "event": "opec_production_cut",
            "corridor": "global",
            "probability": 35,
            "duration_days": 90,
            "precedent": "Similar to 2023 OPEC+ production cuts",
            "confidence": "low",
            "summary": "OPEC+ production adjustments could impact global crude supply to India",
            "source": "",
        }
    return {
        "event": "general_disruption",
        "corridor": "global",
        "probability": 25,
        "duration_days": 30,
        "precedent": "",
        "confidence": "low",
        "summary": "Unspecified energy supply disruption signal detected",
        "source": "",
    }


async def process_articles(articles: list[dict]) -> list[dict]:
    signals = []
    for article in articles:
        signal = await extract_signal(
            title=article.get("title", ""),
            description=article.get("description", ""),
            content=article.get("content", article.get("description", "")),
            source=article.get("source", {}).get("name", "Unknown"),
            published_at=article.get("publishedAt", ""),
        )
        signals.append(signal)
    return signals
