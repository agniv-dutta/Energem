from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


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


class ResilienceDependency(BaseModel):
    supplier: str
    dependency_percent: float
    risk: str
    notes: str


class MitigationPriority(BaseModel):
    priority: int
    action: str
    impact: str
    timeline_days: int


class ResilienceResponse(BaseModel):
    resilience_score: int
    resilience_level: str
    vulnerability_ranking: int
    vulnerability_notes: str
    critical_dependencies: list[ResilienceDependency]
    time_to_critical_reserve_days: float
    recovery_time_days: float
    recovery_notes: str
    mitigation_priorities: list[MitigationPriority]
    key_weaknesses: list[str]
    key_strengths: list[str]
    summary: str


class RiskZone(BaseModel):
    zone_name: str
    region: str
    risk_level: str
    risk_score: float
    latitude: float
    longitude: float
    radius_km: float
    description: str
    threats: list[str]
    affected_routes: list[str]


class VulnerableRoute(BaseModel):
    route_name: str
    from_field: str = Field("", alias="from")
    to_field: str = Field("", alias="to")
    risk_level: str
    latitude_start: list[float]
    latitude_end: list[float]
    length_km: float
    chokepoints: list[str]
    alternatives: list[str]

    model_config = {"populate_by_name": True}


class Hotspot(BaseModel):
    name: str
    type: str
    latitude: float
    longitude: float
    priority: str


class ContingencyInfra(BaseModel):
    type: str
    recommended_location: str
    latitude: float
    longitude: float
    justification: str
    priority: str


class PatrolZone(BaseModel):
    zone: str
    priority: str
    assets_required: str
    coverage_radius_km: float


class GeospatialResponse(BaseModel):
    risk_zones: list[RiskZone]
    vulnerable_routes: list[VulnerableRoute]
    hotspots: list[Hotspot]
    contingency_infrastructure: list[ContingencyInfra]
    patrol_distribution: list[PatrolZone]
    overall_heatmap_summary: str


class CountryProfile(BaseModel):
    name: str
    import_dependency_percent: float
    primary_chokepoints: list[str]
    vulnerability_score: int
    vulnerability_profile: str
    spr_days: float
    diversification_score: int
    resilience_strategies: list[str]
    response_protocols: str
    effectiveness_rating: str
    effectiveness_notes: str
    key_lessons: list[str]


class ComparisonMatrix(BaseModel):
    columns: list[str]
    rows: list[list[str]]


class CountryComparisonResponse(BaseModel):
    countries: list[CountryProfile]
    comparison_matrix: ComparisonMatrix
    lessons_for_india: list[str]
    top_recommendation: str
    summary: str


class EscalationResponse(BaseModel):
    trajectory: str
    trajectory_confidence: str
    escalation_score: int
    risk_level: str
    critical_trigger: Optional[str] = None
    historical_precedent: Optional[str] = None
    de_escalation_path: Optional[str] = None
    probability_military_action_7_days: float
    probability_military_action_14_days: float
    probability_military_action_30_days: float
    timeline_to_potential_action: str
    affected_corridors: list[str]
    key_actors: list[str]
    summary: str


class DashboardResponse(BaseModel):
    risk: RiskResponse
    signals: list[SignalResponse]
    market_data: MarketDataResponse
    primary_scenario: Optional[ScenarioResponse] = None
    recommendations: Optional[RecommendationResponse] = None
    timestamp: str
