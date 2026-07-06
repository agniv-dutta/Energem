from math import ceil

HORMUZ_FLOW_BBL = 1_500_000
DAILY_CONSUMPTION = 4_500_000
MAX_DRAWDOWN = 500_000
BASE_SPR = 9.3
BASE_BRENT = 95.0
BRENT_CEILING = 150.0
NORMAL_UTIL = 0.90
DEMAND_ELASTICITY = -0.1
ALT_RUSSIA = 300_000
ALT_BRAZIL = 200_000
ALT_SPOT = 500_000
ALT_TOTAL = ALT_RUSSIA + ALT_BRAZIL + ALT_SPOT

CHECK_DAYS = [1, 5, 10, 30]

CORRIDOR_NAMES = {
    "hormuz": "Strait of Hormuz",
    "red_sea": "Red Sea / Bab al-Mandab",
    "suez": "Suez Canal",
    "malacca": "Malacca Strait",
}


def simulate(
    corridor="hormuz",
    disruption_percent=50,
    duration_days=30,
    affected_nodes=None,
    scenario_name="",
    alternatives_activated=True,
):
    if affected_nodes is None:
        affected_nodes = ["GULF_STREAM_PIPE_01", "PORT_ARTHUR_REFINERY"]

    frac = disruption_percent / 100.0
    daily_loss = int(frac * HORMUZ_FLOW_BBL)

    timeline = []
    flags = []
    prev_price = BASE_BRENT
    cumulative = 0
    alt_active = False
    recovery_note = None
    spr_critical_flagged = False
    stress_flagged = False

    for day in range(1, duration_days + 1):
        cumulative += daily_loss

        drawdown = min(daily_loss, MAX_DRAWDOWN)
        spr_rem = round(max(BASE_SPR - (drawdown * day / DAILY_CONSUMPTION), 0.0), 1)

        price = round(min(BASE_BRENT * 1.10 + BASE_BRENT * frac * 0.005 * (day - 1), BRENT_CEILING), 1)
        prev_price = price

        price_mult = price / BASE_BRENT
        util = round((NORMAL_UTIL + DEMAND_ELASTICITY * (price_mult - 1)) * 100, 1)
        util = max(50.0, min(100.0, util))

        if alternatives_activated and day >= 20 and not alt_active:
            alt_active = True

        supply_loss_display = daily_loss
        if alt_active:
            recoverable = min(ALT_TOTAL, daily_loss)
            supply_loss_display = daily_loss - recoverable

        if day == duration_days:
            if alt_active or alternatives_activated:
                remaining = cumulative - sum(
                    min(ALT_TOTAL, daily_loss) for _ in range(max(0, duration_days - 19))
                ) if duration_days > 19 else cumulative
                recovery_days = ceil(remaining / ALT_TOTAL) if ALT_TOTAL > 0 else 999
                recovery_note = f"{recovery_days} days (with alternatives)"
            else:
                recovery_note = "No recovery without action"

        confidence_lo = round(max(0, price * 0.90), 1)
        confidence_hi = round(min(BRENT_CEILING, price * 1.10), 1)

        if spr_rem < 7 and not spr_critical_flagged:
            flags.append({"day": day, "severity": "CRITICAL", "message": "CRITICAL — ACTIVATE SPR IMMEDIATELY"})
            spr_critical_flagged = True

        timeline.append({
            "day": day,
            "supply_loss_bbl": supply_loss_display,
            "spr_remaining_days": spr_rem,
            "brent_price": price,
            "brent_price_range": [confidence_lo, confidence_hi],
            "refinery_utilization_pct": util,
            "cumulative_deficit_bbl": cumulative,
            "flags": [],
        })

    if duration_days > 30 and not alternatives_activated:
        flags.append({"day": duration_days, "severity": "WARNING", "message": "SPR EXHAUSTION RISK — duration > 30d without alternatives"})

    peak_price = max(t["brent_price"] for t in timeline)
    if peak_price >= 140 and not stress_flagged:
        stress_day = next(t["day"] for t in timeline if t["brent_price"] >= 140)
        flags.append({"day": stress_day, "severity": "WARNING", "message": "ECONOMIC STRESS — DEMAND DESTRUCTION LIKELY"})
        stress_flagged = True

    display = [t for t in timeline if t["day"] in CHECK_DAYS]
    for t in display:
        day_flags = [f["message"] for f in flags if f["day"] <= t["day"]]
        t["flags"] = day_flags

    last_spr = display[-1]["spr_remaining_days"] if display else BASE_SPR

    recommended = []
    if disruption_percent > 20:
        recommended.append("increase_russia")
    if last_spr < 7:
        recommended.append("activate_spr")
    if disruption_percent > 30:
        recommended.append("spot_market")
        recommended.append("diversify_suppliers")
    if duration_days > 15:
        recommended.append("long_term_contracts")
        recommended.append("demand_side_measures")

    return {
        "scenario": scenario_name or f"{CORRIDOR_NAMES.get(corridor, corridor)} {disruption_percent:.0f}% closure, {duration_days} days",
        "parameters": {
            "corridor": corridor,
            "disruption_percent": disruption_percent,
            "duration_days": duration_days,
            "affected_nodes": affected_nodes,
            "alternatives_activated": alternatives_activated,
            "daily_loss_bbl": daily_loss,
        },
        "timeline": display,
        "summary": {
            "total_deficit_bbl": cumulative,
            "total_deficit_display": _fmt_bbl(cumulative),
            "peak_price": round(peak_price, 1),
            "peak_price_display": f"${round(peak_price, 1)}/barrel",
            "spr_critical_day": _spr_critical_day(timeline),
            "gdp_impact_annualized_pct": round(-0.3 * (disruption_percent / 50), 2),
            "recovery_estimate": recovery_note,
            "recommended_actions": recommended,
        },
        "flags": flags,
        "uncertainty_note": "Confidence ranges reflect ±10% due to geopolitical volatility",
    }


def _fmt_bbl(bbl):
    if bbl >= 1_000_000:
        return f"{bbl / 1_000_000:.1f}M BBL"
    if bbl >= 1_000:
        return f"{bbl / 1_000:.0f}K BBL"
    return f"{bbl} BBL"


def _spr_critical_day(timeline):
    for t in timeline:
        if t["spr_remaining_days"] < 5:
            return t["day"]
    return timeline[-1]["day"] if timeline else 0
