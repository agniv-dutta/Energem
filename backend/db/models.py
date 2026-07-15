from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Integer, Float, String, DateTime, JSON, Text, ForeignKey, UniqueConstraint
from backend.db.session import Base


class Article(Base):
    __tablename__ = "articles"
    __table_args__ = (
        UniqueConstraint("source", "published_at", name="uq_articles_source_published_at"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(255), nullable=False, index=True)
    headline = Column(Text, nullable=False)
    body = Column(Text)
    published_at = Column(DateTime, nullable=False, index=True)
    raw_json = Column(JSON, nullable=False)
    url = Column(Text)
    extraction_status = Column(String(40), nullable=False, default="pending")
    retry_after = Column(DateTime)
    last_error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False)
    corridor = Column(String(50), nullable=False, index=True)
    probability = Column(Float, nullable=False)
    duration_days = Column(Float)
    confidence = Column(String(20), nullable=False)
    extracted_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class RiskSnapshot(Base):
    __tablename__ = "risk_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    composite_score = Column(Float, nullable=False)
    corridor_scores = Column(JSON, nullable=False)
    signals_count = Column(Integer, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow, index=True)
    confidence = Column(String(20), nullable=False)


class RiskSignal(Base):
    __tablename__ = "risk_signals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event = Column(String(255), nullable=False)
    corridor = Column(String(100), nullable=False)
    probability = Column(Float, nullable=False)
    duration_days = Column(Float)
    precedent = Column(Text)
    confidence = Column(String(20), nullable=False)
    summary = Column(Text)
    source = Column(String(255))
    raw_article = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Corridor(Base):
    __tablename__ = "corridors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    corridor_id = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    key_value = Column(String(50), nullable=False, index=True)
    baseline_daily_flow_bbl = Column(Integer, nullable=False)
    historical_baseline_risk = Column(Float, nullable=False, default=50.0)
    alternative_routes = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class CorridorRisk(Base):
    __tablename__ = "corridor_risks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    corridor = Column(String(100), nullable=False)
    scenario = Column(String(255), nullable=False)
    probability_percent = Column(Float, nullable=False)
    impact_percent = Column(Float, nullable=False)
    composite_risk = Column(Float, nullable=False)
    confidence = Column(String(20), nullable=False)
    brent_price = Column(Float)
    spr_days = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scenario_name = Column(String(255), nullable=False)
    disruption_type = Column(String(100), nullable=False)
    duration_days = Column(Integer, nullable=False)
    probability_percent = Column(Float, nullable=False)
    supply_loss_percent = Column(Float)
    impact_timeline = Column(JSON)
    price_impact = Column(Float)
    refinery_impact_percent = Column(Float)
    gdp_impact_percent = Column(Float)
    assumptions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    scenario_id = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)
    action = Column(Text, nullable=False)
    supplier = Column(Text)
    volume_bbl_per_day = Column(Integer)
    eta_days = Column(Integer)
    cost_premium_per_barrel = Column(Float)
    geopolitical_risk = Column(String(20))
    confidence = Column(Integer)
    reasoning = Column(Text)
    status = Column(String(30), nullable=False, default="generated")
    approved_by = Column(String(255))
    approved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    timeline_days = Column(Integer)
    volume_bbl = Column(Float)


class AuthorizationLog(Base):
    __tablename__ = "authorization_log"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    recommendation_id = Column(String(36), ForeignKey("recommendations.id"), nullable=False, index=True)
    action = Column(String(20), nullable=False)
    authorized_by = Column(String(255), nullable=False)
    reason = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
