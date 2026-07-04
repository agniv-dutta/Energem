import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.config import get_settings

settings = get_settings()

RESILIENCE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an energy security officer for Energem, an energy supply chain resilience system for India.
Rate India's crude oil supply chain resilience against the current disruption scenario.

Portfolio: Saudi 40%, Iraq 20%, Russia 10%, Brazil 5%, Iran 8%, Others 17%
SPR reserve: 9.5 days
Refinery capacity: 250M tonnes/year
India daily consumption: 5.5M bbl/day
India daily import: 4.8M bbl/day

Score resilience 1-10:
1-3: Critical vulnerability — supply crisis imminent
4-5: Poor resilience — significant disruption expected
6-7: Moderate resilience — can withstand minor shocks
8-9: Good resilience — well diversified and prepared
10: Exceptional — fully resilient

Always output valid JSON only, no markdown formatting."""),
    ("human", """SCENARIO:
{scenario_details}

CURRENT SIGNALS:
{signals}

ANALYZE AND OUTPUT JSON:
{{
  "resilience_score": 1-10,
  "resilience_level": "critical/poor/moderate/good/exceptional",
  "vulnerability_ranking": 1-10,
  "vulnerability_notes": "...",
  "critical_dependencies": [
    {{"supplier": "Saudi Arabia", "dependency_percent": 40, "risk": "high/medium/low", "notes": "..."}}
  ],
  "time_to_critical_reserve_days": N,
  "recovery_time_days": N,
  "recovery_notes": "...",
  "mitigation_priorities": [
    {{"priority": 1, "action": "...", "impact": "high/medium/low", "timeline_days": N}}
  ],
  "key_weaknesses": ["..."],
  "key_strengths": ["..."],
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


async def assess_resilience(scenario_details: str, signals: str = "") -> dict:
    try:
        llm = _get_llm()
        chain = RESILIENCE_PROMPT | llm
        response = await chain.ainvoke({
            "scenario_details": scenario_details[:2000],
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
        return _fallback_resilience(scenario_details, signals)


def _fallback_resilience(scenario_details: str, signals: str) -> dict:
    signals_lower = (scenario_details + " " + signals).lower()

    has_hormuz = "hormuz" in signals_lower
    has_houthi = "houthi" in signals_lower or "red sea" in signals_lower
    has_iran = "iran" in signals_lower or "sanctions" in signals_lower
    severity = sum([has_hormuz, has_houthi, has_iran])

    if severity >= 2:
        score = 4
        level = "poor"
        vuln = 8
        critical_days = 7
        recovery = 21
    elif severity == 1:
        score = 6
        level = "moderate"
        vuln = 6
        critical_days = 10
        recovery = 14
    else:
        score = 7
        level = "moderate"
        vuln = 5
        critical_days = 12
        recovery = 10

    return {
        "resilience_score": score,
        "resilience_level": level,
        "vulnerability_ranking": vuln,
        "vulnerability_notes": "India's 88% import dependency and 43% Hormuz concentration create structural vulnerability",
        "critical_dependencies": [
            {"supplier": "Saudi Arabia", "dependency_percent": 40, "risk": "high", "notes": "Single largest supplier; Hormuz-dependent"},
            {"supplier": "Iraq", "dependency_percent": 20, "risk": "high", "notes": "Second largest; also Hormuz-dependent"},
            {"supplier": "Iran", "dependency_percent": 8, "risk": "high", "notes": "Under sanctions; unreliable supply"},
            {"supplier": "Russia", "dependency_percent": 10, "risk": "medium", "notes": "Sanctions risk but non-Hormuz route"},
            {"supplier": "Brazil", "dependency_percent": 5, "risk": "low", "notes": "Diversification; long transit time"},
        ],
        "time_to_critical_reserve_days": critical_days,
        "recovery_time_days": recovery,
        "recovery_notes": "Recovery depends on alternative sourcing speed (10-14 days) and Hormuz reopening timeline",
        "mitigation_priorities": [
            {
                "priority": 1,
                "action": "Diversify away from Hormuz-dependent suppliers (Saudi, Iraq) toward Brazil, West Africa, US",
                "impact": "high",
                "timeline_days": 90,
            },
            {
                "priority": 2,
                "action": "Increase SPR capacity from 9.5 to minimum 30 days of consumption",
                "impact": "high",
                "timeline_days": 365,
            },
            {
                "priority": 3,
                "action": "Develop strategic storage at destination ports (beyond SPR) for 15 days of supply",
                "impact": "medium",
                "timeline_days": 180,
            },
            {
                "priority": 4,
                "action": "Negotiate emergency supply agreements with Russia, Brazil, and US for crisis scenarios",
                "impact": "high",
                "timeline_days": 45,
            },
            {
                "priority": 5,
                "action": "Invest in domestic refining capacity for alternative crude grades (Russian Urals, Brazilian Tupi)",
                "impact": "medium",
                "timeline_days": 180,
            },
        ],
        "key_weaknesses": [
            "88% import dependency with no near-term substitute",
            "43% of imports transit Hormuz single-point-of-failure",
            "SPR only 9.5 days — among lowest for major economies",
            "Over-reliance on two suppliers (Saudi + Iraq = 60%)",
        ],
        "key_strengths": [
            "Refinery capacity sufficient for domestic needs",
            "Russia and Brazil provide non-Hormuz alternatives",
            "Government has demonstrated ability to execute emergency procurement",
        ],
        "summary": f"Resilience score {score}/10 ({level}). India's supply chain can withstand minor disruptions but is critically vulnerable to a major Hormuz event. SPR at 9.5 days is dangerously low — needs immediate diversification and reserve expansion.",
    }
