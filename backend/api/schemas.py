from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SignalResponse(BaseModel):
    event: str
    corridor: str
    probability: float
    duration_days: Optional[float] = None
    precedent: Optional[str] = None
    confidence: str
    summary: Optional[str] = None
    source: Optional[str] = None


class CorridorRiskResponse(BaseModel):
    corridor: str
    scenario: str
    probability_percent: float
    impact_percent: float
    composite_risk: float
    confidence: str


class RiskResponse(BaseModel):
    corridors: list[CorridorRiskResponse]
    overall_risk_score: float
    primary_threat: str
    risk_level: str


class TimelinePoint(BaseModel):
    supply_gap_bbl: int
    spr_drain_days: float
    brent_price: float
    refinery_impact_percent: float


class ScenarioResponse(BaseModel):
    scenario_name: str
    disruption_type: str
    duration_days: int
    supply_loss_percent: float
    impact_timeline: dict[str, TimelinePoint]
    price_impact_multiplier: float
    gdp_impact_percent: float
    assumptions: list[str]
    confidence: str


class RecommendationItem(BaseModel):
    priority: int
    action: str
    timeline_days: int
    volume_bbl: int
    cost_premium_dollars_per_barrel: float
    geopolitical_risk: str
    confidence: str
    reasoning: Optional[str] = None


class RecommendationResponse(BaseModel):
    scenario: str
    supply_gap_bbl: int
    recommendations: list[RecommendationItem]
    composite_strategy: Optional[str] = None
    estimated_total_cost_premium: Optional[float] = None


class MarketDataResponse(BaseModel):
    brent_crude: dict
    wti_crude: Optional[dict] = None
    natural_gas: Optional[dict] = None


class NewsQuery(BaseModel):
    query: str = "energy supply disruption oil"
    page_size: int = 5


class ScenarioQuery(BaseModel):
    scenario: str = "Hormuz Partial Closure (30%)"
    duration_days: int = 30
    supply_loss_percent: float = 30
    brent_price: float = 95.00
    spr_days: float = 9.5


class RecommendQuery(BaseModel):
    scenario: str = "Hormuz Partial Closure (30%)"
    supply_gap: int = 500000
    brent_price: float = 95.00
    confidence: str = "medium"


class DashboardResponse(BaseModel):
    risk: RiskResponse
    signals: list[SignalResponse]
    market_data: MarketDataResponse
    primary_scenario: Optional[ScenarioResponse] = None
    recommendations: Optional[RecommendationResponse] = None
    timestamp: str
