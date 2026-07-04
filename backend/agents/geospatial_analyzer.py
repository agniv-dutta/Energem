import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from backend.config import get_settings

settings = get_settings()

GEOSPATIAL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a GIS analyst for Energem, an energy supply chain resilience system for India.
Create a risk heat map description for India's crude oil supply routes.

Output valid JSON only, no markdown formatting."""),
    ("human", """CURRENT RISK SCORES BY CORRIDOR:
{risk_scores}

INFRASTRUCTURE:
- Refineries: {refineries}
- SPR depots: Visakhapatnam (1.33M tonnes), Mangalore (1.5M tonnes), Padur (2.5M tonnes)
- Major ports: Mundra, Kandla, Mumbai, Chennai, Vishakhapatnam, Paradip

ANALYZE AND OUTPUT JSON:
{{
  "risk_zones": [
    {{
      "zone_name": "...",
      "region": "...",
      "risk_level": "critical/high/medium/low",
      "risk_score": 0-100,
      "latitude": N,
      "longitude": N,
      "radius_km": N,
      "description": "...",
      "threats": ["..."],
      "affected_routes": ["..."]
    }}
  ],
  "vulnerable_routes": [
    {{
      "route_name": "...",
      "from": "...",
      "to": "...",
      "risk_level": "critical/high/medium/low",
      "latitude_start": [N, N],
      "latitude_end": [N, N],
      "length_km": N,
      "chokepoints": ["..."],
      "alternatives": ["..."]
    }}
  ],
  "hotspots": [
    {{
      "name": "...",
      "type": "port/refinery/chokepoint/spr_depot",
      "latitude": N,
      "longitude": N,
      "priority": "high/medium/low"
    }}
  ],
  "contingency_infrastructure": [
    {{
      "type": "spr_storage/port/refinery/alternate_route",
      "recommended_location": "...",
      "latitude": N,
      "longitude": N,
      "justification": "...",
      "priority": "high/medium/low"
    }}
  ],
  "patrol_distribution": [
    {{
      "zone": "...",
      "priority": "critical/high/medium",
      "assets_required": "...",
      "coverage_radius_km": N
    }}
  ],
  "overall_heatmap_summary": "..."
}}"""),
])


def _get_llm():
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )


async def analyze_geospatial(
    risk_scores: list[dict],
    refineries: str = "Jamnagar (22.2N, 69.7E), Reliance (21.4N, 72.1E), Mumbai (19.1N, 72.9E), Chennai (13.1N, 80.3E), Paradip (20.3N, 86.7E), Visakhapatnam (17.7N, 83.3E), Kochi (9.9N, 76.3E), Bina (23.9N, 78.1E), Panipat (29.4N, 76.9E), Numaligarh (26.6N, 93.7E)",
) -> dict:
    try:
        llm = _get_llm()
        chain = GEOSPATIAL_PROMPT | llm
        risk_text = "\n".join(
            f"- {r.get('corridor', 'N/A')}: {r.get('composite_risk', r.get('risk_score', 50))}/100 — {r.get('scenario', r.get('risk_level', 'moderate'))}"
            for r in risk_scores
        )
        response = await chain.ainvoke({
            "risk_scores": risk_text,
            "refineries": refineries,
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
        return _fallback_geospatial(risk_scores)


def _fallback_geospatial(risk_scores: list[dict]) -> dict:
    hormone_score = 65
    red_sea_score = 55
    suez_score = 35
    malacca_score = 25
    for r in risk_scores:
        c = r.get("corridor", "").lower()
        s = r.get("composite_risk", r.get("risk_score", 50))
        if "hormuz" in c:
            hormone_score = s
        elif "red" in c:
            red_sea_score = s
        elif "suez" in c:
            suez_score = s
        elif "malacca" in c:
            malacca_score = s

    return {
        "risk_zones": [
            {
                "zone_name": "Strait of Hormuz",
                "region": "Persian Gulf / Gulf of Oman",
                "risk_level": "critical" if hormone_score >= 60 else "high",
                "risk_score": hormone_score,
                "latitude": 26.5,
                "longitude": 56.0,
                "radius_km": 200,
                "description": "Primary chokepoint for Indian crude — 43% of imports transit here",
                "threats": ["Iran military escalation", "Houthi missile attacks", "Tanker seizures", "Naval mine deployment"],
                "affected_routes": ["Persian Gulf → Gulf of Oman → Arabian Sea"],
            },
            {
                "zone_name": "Bab al-Mandab / Red Sea",
                "region": "Yemen / Djibouti coast",
                "risk_level": "high" if red_sea_score >= 50 else "medium",
                "risk_score": red_sea_score,
                "latitude": 13.5,
                "longitude": 43.5,
                "radius_km": 150,
                "description": "Alternative route chokepoint threatened by Houthi attacks",
                "threats": ["Houthi missile attacks", "Drone strikes on tankers", "Piracy"],
                "affected_routes": ["Mediterranean → Suez → Red Sea → Indian Ocean"],
            },
            {
                "zone_name": "Suez Canal",
                "region": "Egypt",
                "risk_level": "medium",
                "risk_score": suez_score,
                "latitude": 30.5,
                "longitude": 32.5,
                "radius_km": 100,
                "description": "Strategic canal transit — political instability risk",
                "threats": ["Political instability", "Terrorism", "Transit fee disputes"],
                "affected_routes": ["Europe → Suez → Red Sea → Indian Ocean"],
            },
            {
                "zone_name": "Malacca Strait",
                "region": "Indonesia / Malaysia / Singapore",
                "risk_level": "low",
                "risk_score": malacca_score,
                "latitude": 2.0,
                "longitude": 102.0,
                "radius_km": 150,
                "description": "Alternative eastern route — generally safe but congested",
                "threats": ["Piracy", "Congestion", "Geopolitical tension"],
                "affected_routes": ["Pacific → Malacca → Indian Ocean"],
            },
            {
                "zone_name": "Western Indian Coast",
                "region": "Gujarat / Maharashtra",
                "risk_level": "medium",
                "risk_score": 40,
                "latitude": 20.0,
                "longitude": 72.0,
                "radius_km": 300,
                "description": "Primary offloading zone — Mundra, Kandla, Mumbai ports",
                "threats": ["Port congestion", "Refinery concentration risk"],
                "affected_routes": ["All import routes converging to west coast"],
            },
        ],
        "vulnerable_routes": [
            {
                "route_name": "Persian Gulf → Hormuz → Gujarat",
                "from": "Ras Tanura (Saudi Arabia)",
                "to": "Mundra / Kandla (India)",
                "risk_level": "critical",
                "latitude_start": [26.5, 56.0],
                "latitude_end": [22.8, 69.5],
                "length_km": 2200,
                "chokepoints": ["Strait of Hormuz (34km wide)"],
                "alternatives": ["Red Sea → Suez → Mediterranean (longer)", "Malacca Strait → Bay of Bengal"],
            },
            {
                "route_name": "West Africa → Cape of Good Hope → India",
                "from": "Luanda (Angola)",
                "to": "Kochi / Chennai (India)",
                "risk_level": "low",
                "latitude_start": [-8.8, 13.2],
                "latitude_end": [9.9, 76.3],
                "length_km": 9000,
                "chokepoints": ["Cape of Good Hope"],
                "alternatives": ["Direct Atlantic → Indian Ocean"],
            },
            {
                "route_name": "Russia (Baltic) → North Sea → Suez → India",
                "from": "Primorsk (Russia)",
                "to": "Vishakhapatnam (India)",
                "risk_level": "medium",
                "latitude_start": [60.0, 28.0],
                "latitude_end": [17.7, 83.3],
                "length_km": 12000,
                "chokepoints": ["Suez Canal", "Danish Straits"],
                "alternatives": ["Arctic route (seasonal)", "Trans-Siberian rail"],
            },
        ],
        "hotspots": [
            {"name": "Jamnagar Refinery", "type": "refinery", "latitude": 22.2, "longitude": 69.7, "priority": "high"},
            {"name": "Mundra Port", "type": "port", "latitude": 22.8, "longitude": 69.5, "priority": "high"},
            {"name": "Kandla Port", "type": "port", "latitude": 23.0, "longitude": 70.1, "priority": "high"},
            {"name": "SPR Padur", "type": "spr_depot", "latitude": 12.9, "longitude": 74.8, "priority": "high"},
            {"name": "SPR Visakhapatnam", "type": "spr_depot", "latitude": 17.7, "longitude": 83.3, "priority": "high"},
            {"name": "Mumbai Port", "type": "port", "latitude": 19.1, "longitude": 72.9, "priority": "high"},
        ],
        "contingency_infrastructure": [
            {
                "type": "spr_storage",
                "recommended_location": "Eastern coast — Paradip or Vizag",
                "latitude": 20.3,
                "longitude": 86.7,
                "justification": "All SPR currently on west coast; east coast storage hedges against Hormuz disruption",
                "priority": "high",
            },
            {
                "type": "port",
                "recommended_location": "Port Blair (Andaman Islands)",
                "latitude": 11.6,
                "longitude": 92.7,
                "justification": "Strategic location for monitoring Malacca traffic and emergency transshipment",
                "priority": "medium",
            },
            {
                "type": "alternate_route",
                "recommended_location": "Chabahar port (Iran) — India-developed",
                "latitude": 25.3,
                "longitude": 60.6,
                "justification": "Alternative access to Central Asia, bypasses Hormuz for some supply",
                "priority": "high",
            },
            {
                "type": "refinery",
                "recommended_location": "Eastern coast — Paradip expansion",
                "latitude": 20.3,
                "longitude": 86.7,
                "justification": "Reduce refinery concentration on west coast; process alternative crudes (Russia, Brazil)",
                "priority": "medium",
            },
        ],
        "patrol_distribution": [
            {
                "zone": "Strait of Hormuz — Persian Gulf",
                "priority": "critical",
                "assets_required": "2x naval destroyers, 4x patrol vessels, maritime patrol aircraft",
                "coverage_radius_km": 200,
            },
            {
                "zone": "Arabian Sea — Western approaches",
                "priority": "high",
                "assets_required": "1x frigate, 2x offshore patrol vessels, P-8I surveillance",
                "coverage_radius_km": 300,
            },
            {
                "zone": "Gulf of Aden — Red Sea approach",
                "priority": "high",
                "assets_required": "2x patrol vessels, drone surveillance (MQ-9)",
                "coverage_radius_km": 150,
            },
            {
                "zone": "Malacca Strait — Eastern approaches",
                "priority": "medium",
                "assets_required": "2x patrol vessels, cooperation with Indonesia/Malaysia",
                "coverage_radius_km": 100,
            },
        ],
        "overall_heatmap_summary": f"Critical risk zone centered on Hormuz (score {hormone_score}/100) extending through Persian Gulf and Arabian Sea. West coast infrastructure (Mundra, Kandla, Mumbai, Jamnagar) is dangerously concentrated. Recommend east coast SPR expansion and enhanced naval patrols in western approaches.",
    }
