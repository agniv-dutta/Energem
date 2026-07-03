HISTORICAL_DISRUPTIONS = [
    {
        "event": "2022 Houthi Red Sea attacks",
        "year": 2022,
        "corridor": "red_sea",
        "duration_days": 180,
        "impact": "Shipping delays of 2-3 weeks, insurance premiums +500%",
        "outcome": "Partial resolution through ceasefire, but sporadic attacks continued",
    },
    {
        "event": "2019 Hormuz tanker crisis",
        "year": 2019,
        "corridor": "hormuz",
        "duration_days": 60,
        "impact": "Brent crude +15%, insurance premiums spiked, tanker traffic reduced 25%",
        "outcome": "De-escalation after diplomatic engagement; no full closure",
    },
    {
        "event": "1973 Arab oil embargo",
        "year": 1973,
        "corridor": "hormuz",
        "duration_days": 180,
        "impact": "Oil prices +400%, global recession, permanent shift in energy policy",
        "outcome": "Embargo lifted after diplomatic resolution; led to creation of IEA and SPRs",
    },
    {
        "event": "2020 Saudi-Russia price war",
        "year": 2020,
        "corridor": "global",
        "duration_days": 60,
        "impact": "Brent crude crashed to $20/barrel, production cuts of 10M bbl/day",
        "outcome": "OPEC+ agreement restored stability after 2 months",
    },
    {
        "event": "2023 OPEC+ production cuts",
        "year": 2023,
        "corridor": "global",
        "duration_days": 365,
        "impact": "Brent crude sustained at $85-95/barrel, supply reduction of 2M bbl/day",
        "outcome": "Cuts extended through 2024, maintaining price floor",
    },
    {
        "event": "2005-2006 Iran nuclear crisis",
        "year": 2005,
        "corridor": "hormuz",
        "duration_days": 365,
        "impact": "Geopolitical premium of $5-10/barrel on Brent, no physical disruption",
        "outcome": "Diplomatic resolution without military conflict",
    },
]


async def get_historical_precedent(corridor: str = None, event_type: str = None) -> list[dict]:
    results = HISTORICAL_DISRUPTIONS
    if corridor:
        results = [d for d in results if d["corridor"] == corridor]
    if event_type:
        results = [d for d in results if event_type.lower() in d["event"].lower()]
    return results
