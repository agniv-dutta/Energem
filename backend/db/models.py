from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, JSON, Text
from backend.db.session import Base


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

    id = Column(Integer, primary_key=True, autoincrement=True)
    scenario_id = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)
    action = Column(Text, nullable=False)
    timeline_days = Column(Integer)
    volume_bbl = Column(Float)
    cost_premium_per_barrel = Column(Float)
    geopolitical_risk = Column(String(20))
    confidence = Column(String(20))
    reasoning = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
