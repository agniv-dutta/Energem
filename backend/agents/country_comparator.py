import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.config import get_settings

settings = get_settings()

COMPARISON_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a comparative energy security analyst for Energem.
Compare energy supply chain resilience across import-dependent countries.

Output valid JSON only, no markdown formatting."""),
    ("human", """CURRENT GLOBAL CONTEXT:
{context}

For each country (India, Japan, South Korea, Turkey), analyze:
1. Vulnerability profile — chokepoints, dependencies, key risks
2. Resilience strategies — SPR, diversification, alternatives
3. Response protocols — government + industry coordination
4. Effectiveness — how strategies have performed historically

OUTPUT JSON:
{{
  "countries": [
    {{
      "name": "India",
      "import_dependency_percent": 88,
      "primary_chokepoints": ["Hormuz"],
      "vulnerability_score": 1-10,
      "vulnerability_profile": "...",
      "spr_days": N,
      "diversification_score": 1-10,
      "resilience_strategies": ["..."],
      "response_protocols": "...",
      "effectiveness_rating": "high/medium/low",
      "effectiveness_notes": "...",
      "key_lessons": ["..."]
    }}
  ],
  "comparison_matrix": {{
    "columns": ["Country", "Import Dependency", "Hormuz Dependency", "SPR Days", "Vulnerability", "Diversification", "Effectiveness"],
    "rows": [
      ["India", "88%", "43%", "9.5", "...", "...", "..."]
    ]
  }},
  "lessons_for_india": ["..."],
  "top_recommendation": "...",
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


async def compare_countries(context: str = "") -> dict:
    try:
        llm = _get_llm()
        chain = COMPARISON_PROMPT | llm
        response = await chain.ainvoke({"context": context[:2000] or "Current geopolitical tensions affecting global energy supply chains"})
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
        return _fallback_comparison()


def _fallback_comparison() -> dict:
    return {
        "countries": [
            {
                "name": "India",
                "import_dependency_percent": 88,
                "primary_chokepoints": ["Hormuz", "Malacca"],
                "vulnerability_score": 8,
                "vulnerability_profile": "Extreme reliance on Hormuz (43% of imports). SPR at 9.5 days — lowest among peers. Limited diversification (Saudi+Iraq=60%). Refinery concentration on vulnerable west coast.",
                "spr_days": 9.5,
                "diversification_score": 3,
                "resilience_strategies": [
                    "SPR program (Visakhapatnam, Mangalore, Padur — 5.33M tonnes)",
                    "Russia and Brazil sourcing to reduce Hormuz dependence",
                    "Refinery capacity expansion (250M tonnes/year)",
                    "Chabahar port development for alternate access",
                ],
                "response_protocols": "Government-led through Ministry of Petroleum; coordination with IOC, BPCL, HPCL; SPR releases require Cabinet approval — estimated 48-72 hr decision cycle",
                "effectiveness_rating": "low",
                "effectiveness_notes": "2022 Russia discount: India increased Russian imports from 2% to 35% of total, demonstrating agility. However, SPR at 9.5 days is critically low — would last only 7-10 days under full Hormuz closure.",
                "key_lessons": [
                    "SPR must expand to minimum 30 days",
                    "Hormuz dependency is a single-point-of-failure",
                    "Russia pivot shows ability to execute rapid diversification",
                ],
            },
            {
                "name": "Japan",
                "import_dependency_percent": 95,
                "primary_chokepoints": ["Hormuz", "Malacca", "South China Sea"],
                "vulnerability_score": 9,
                "vulnerability_profile": "Extreme import dependency (95%). Almost all oil transits Hormuz and Malacca. Limited domestic production. Strategic vulnerability to China blockade of South China Sea.",
                "spr_days": 180,
                "diversification_score": 7,
                "resilience_strategies": [
                    "Largest SPR among peers (180+ days — government + private)",
                    "IEA membership provides collective security framework",
                    "Strong nuclear fleet (reduced oil dependency historically)",
                    "Active investment in upstream assets abroad (Japan's trading houses)",
                ],
                "response_protocols": "IEA-coordinated emergency response; METI leads with industry association coordination; 3-tier SPR release (IEA coordinated → government → private); decision cycle < 24 hours",
                "effectiveness_rating": "high",
                "effectiveness_notes": "1973 oil shock triggered massive SPR buildup (9.5 days → 180+ days). 1991 Gulf War demonstrated effective IEA coordination. Fukushima shifted energy policy but oil resilience remains strong.",
                "key_lessons": [
                    "Political will can build SPR from 9 to 180 days within a decade",
                    "IEA membership provides critical crisis coordination",
                    "Government-private partnership models work for strategic storage",
                ],
            },
            {
                "name": "South Korea",
                "import_dependency_percent": 92,
                "primary_chokepoints": ["Hormuz", "Malacca", "South China Sea"],
                "vulnerability_score": 8,
                "vulnerability_profile": "Extreme import dependency (92%). Heavy Hormuz dependence. World's largest LNG importer also vulnerable. Geopolitical risk from North Korea adds layer of complexity.",
                "spr_days": 90,
                "diversification_score": 6,
                "resilience_strategies": [
                    "Substantial SPR (90+ days government + mandatory private reserves)",
                    "IEA membership with collective action framework",
                    "Aggressive upstream investment through KNOC and private sector",
                    "Expanding LNG and renewables to reduce oil dependence",
                ],
                "response_protocols": "IEA framework + Korea National Oil Corporation (KNOC) manages SPR; mandatory industry stockpiling; Cabinet-level Emergency Energy Committee activation",
                "effectiveness_rating": "high",
                "effectiveness_notes": "1991 Gulf War: Korea's IEA membership ensured supply access. 2022 energy crisis: managed through SPR releases and demand controls. SPR system tested and effective.",
                "key_lessons": [
                    "Mandatory private sector stockpiling doubles effective reserves",
                    "IEA membership is a force multiplier for crisis response",
                    "KNOC-style national oil company enables strategic upstream investment",
                ],
            },
            {
                "name": "Turkey",
                "import_dependency_percent": 80,
                "primary_chokepoints": ["Turkish Straits", "Suez", "Russia pipeline"],
                "vulnerability_score": 6,
                "vulnerability_profile": "Lower import dependency (80%) due to some domestic production. Russia-dependent (40%+ of imports). Controls Turkish Straits (geopolitical advantage). Infrastructure vulnerable to earthquakes.",
                "spr_days": 60,
                "diversification_score": 5,
                "resilience_strategies": [
                    "Strategic location as energy corridor (pipelines from Russia, Caspian, Iraq)",
                    "Expanding LNG terminal capacity (can receive US, Qatar, Nigeria cargoes)",
                    "IEA membership provides crisis framework",
                    "Strong refinery capacity (TUPRAS operates 4 refineries)",
                ],
                "response_protocols": "IEA membership + Energy Market Regulatory Authority (EMRA) oversight; SPR managed by TUPRAS and government; rapid LNG market response capability",
                "effectiveness_rating": "medium",
                "effectiveness_notes": "2022 Russia-Ukraine war: Turkey maintained Russian oil imports while complying with sanctions framework. However, dependency on Russia remains a key vulnerability. Earthquake resilience is untested for energy infrastructure.",
                "key_lessons": [
                    "Geographic position can be leveraged as strategic advantage",
                    "LNG diversification provides flexibility against pipeline dependency",
                    "Earthquake resilience must be incorporated into energy planning",
                ],
            },
        ],
        "comparison_matrix": {
            "columns": ["Country", "Import Dependency", "Hormuz Dep.", "SPR Days", "Vulnerability", "Diversification", "IEA Member", "Effectiveness"],
            "rows": [
                ["India", "88%", "43%", "9.5", "8/10", "3/10", "No", "Low"],
                ["Japan", "95%", "85%", "180+", "9/10", "7/10", "Yes", "High"],
                ["South Korea", "92%", "75%", "90+", "8/10", "6/10", "Yes", "High"],
                ["Turkey", "80%", "0% (Russia-dep.)", "60+", "6/10", "5/10", "Yes", "Medium"],
            ],
        },
        "lessons_for_india": [
            "SPR expansion from 9.5 to 90+ days is the single most impactful action — Japan and Korea prove it achievable in 5-10 years",
            "IEA membership (or equivalent bilateral framework) would provide critical crisis coordination and supply-sharing mechanisms",
            "Mandatory private sector stockpiling (used by Korea, Japan) doubles effective reserves at minimal government cost",
            "Diversification away from Hormuz must accelerate — Russia, Brazil, US, West Africa all viable alternatives",
            "National oil company model (KNOC, JOGMEC) enables strategic upstream investment and supply security",
            "Earthquake and climate resilience must be built into energy infrastructure planning (Turkey lesson)",
            "Develop Chabahar and east coast infrastructure as strategic alternatives to west coast concentration",
        ],
        "top_recommendation": "India's most urgent priority is SPR expansion from 9.5 to 90+ days, following the proven model of Japan (achieved post-1973). Combined with IEA membership pursuit and aggressive supplier diversification, this would transform India from most vulnerable to moderately resilient within a decade.",
        "summary": "India is the most vulnerable among peer import-dependent nations. Japan and South Korea demonstrate that 90-180 day SPR reserves are achievable and effective. IEA membership provides critical crisis coordination that India currently lacks. The gap between India and its peers is not structural — it is a policy choice that can be corrected with political will and investment.",
    }
