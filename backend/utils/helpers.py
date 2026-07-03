from datetime import datetime


def format_timestamp(dt: datetime = None) -> str:
    return (dt or datetime.utcnow()).isoformat()


def risk_level_label(score: float) -> str:
    if score <= 20:
        return "low"
    if score <= 40:
        return "moderate"
    if score <= 60:
        return "high"
    if score <= 80:
        return "very_high"
    return "critical"


def truncate_text(text: str, max_length: int = 2000) -> str:
    return text[:max_length] if len(text) > max_length else text


def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"
