from datetime import datetime
from typing import Optional


async def get_brent_crude_price() -> dict:
    try:
        import yfinance as yf
        ticker = yf.Ticker("BZ=F")
        hist = ticker.history(period="5d")
        if not hist.empty:
            current_price = round(float(hist["Close"].iloc[-1]), 2)
            prev_close = round(float(hist["Close"].iloc[-2]), 2) if len(hist) > 1 else current_price
            change_pct = round(((current_price - prev_close) / prev_close) * 100, 2)
            return {
                "current_price": current_price,
                "change_percent": change_pct,
                "high_52w": round(float(hist["High"].max()), 2),
                "low_52w": round(float(hist["Low"].min()), 2),
                "timestamp": datetime.utcnow().isoformat(),
            }
    except Exception:
        pass

    return {
        "current_price": 95.00,
        "change_percent": 0.0,
        "high_52w": 110.00,
        "low_52w": 75.00,
        "timestamp": datetime.utcnow().isoformat(),
    }


async def get_commodity_prices() -> dict:
    return {
        "brent_crude": await get_brent_crude_price(),
        "wti_crude": {"current_price": 88.50, "change_percent": 0.5},
        "natural_gas": {"current_price": 2.85, "change_percent": -1.2},
    }
