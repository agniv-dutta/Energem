# Energy Supply Chain Resilience: Complete Technical Setup Guide

**Decision:** PS #2 — Energy Supply Chain Resilience  
**Timeline:** 20 days to July 22, 2026  
**Solo Build:** Backend + Frontend  

---

## 1. PROJECT NAMING SUGGESTIONS

### Primary Name
**`EnergyGuard`** — Short, memorable, immediately clear purpose  
- GitHub: `energy-guard`
- Tagline: "Real-time energy supply disruption forecasting and resilience orchestration"

### Alternative Names (ranked)
| Name | GitHub Handle | Character Count | Why It Works |
|------|---|---|---|
| **EnergyGuard** | `energy-guard` | 11 chars | Clear, memorable, brand-ready |
| **ResiliencyAI** | `resiliency-ai` | 13 chars | Emphasizes resilience focus |
| **SupplyShield** | `supply-shield` | 13 chars | Defense/protection narrative |
| **HormuzWatch** | `hormuz-watch` | 12 chars | Geopolitically specific |
| **CrudeCompass** | `crude-compass` | 13 chars | Navigation/guidance metaphor |
| **OilSentinel** | `oil-sentinel` | 12 chars | Monitoring/alerting focus |

**Recommendation:** Go with **`EnergyGuard`** — clean, professional, domain-appropriate.

---

## 2. GITHUB REPOSITORY DESCRIPTION (<350 chars)

### Primary (Recommended)
```
AI-powered energy supply chain resilience system for India. Real-time disruption risk 
forecasting using geopolitical signals, maritime tracking & commodity intelligence. 
Predicts energy shocks (Hormuz closure, sanctions, shipping attacks) and recommends 
adaptive procurement strategies. Agentic AI + RAG + scenario modelling.
```
**Character count:** 298 chars ✅

### Alternative (More Technical)
```
Multi-agent LLM system for energy supply chain risk intelligence. Ingests geopolitical 
news, AIS vessel tracking, OFAC sanctions, commodity prices. Detects disruption signals, 
models impact scenarios, recommends procurement alternatives. Addresses India's 88% crude 
import dependency + Hormuz vulnerability.
```
**Character count:** 318 chars ✅

### Alternative (Shorter)
```
Energy supply chain resilience AI for India. Detects geopolitical & logistics disruptions 
(Hormuz closure, sanctions, shipping attacks). Forecasts scenarios + recommends alternative 
sourcing. Multi-agent reasoning over news, shipping data & market signals.
```
**Character count:** 219 chars ✅

---

## 3. EXTERNAL API KEYS REQUIRED

### Critical (Must-Have for MVP)

| API | Purpose | Free Tier | Setup Time | Priority |
|-----|---------|-----------|---|---|
| **OpenAI / Anthropic** | LLM backbone (Claude or GPT-4) | Limited tokens/month | 5 min | 🔴 CRITICAL |
| **NewsAPI** | Geopolitical signal extraction | 100 req/day | 5 min | 🔴 CRITICAL |
| **Yahoo Finance API** | Commodity pricing (Brent crude, spot) | Free/no key sometimes | 5 min | 🔴 CRITICAL |
| **MarineTraffic (AIS)** | Vessel tracking (Hormuz flows) | Paid ($200+/mo) | 10 min | 🟡 MEDIUM |
| **OpenWeatherMap** | Meteorological data (for scenario context) | Free (limited) | 5 min | 🟢 NICE-TO-HAVE |

### Secondary (Enhance Credibility)

| API | Purpose | Free Tier | Setup Time | Priority |
|-----|---------|-----------|---|---|
| **OFAC Sanctions** | US sanctions registry (REST API) | Free/public | 10 min | 🟡 MEDIUM |
| **IEA (International Energy Agency)** | Global energy outlook data | Freemium | 15 min | 🟡 MEDIUM |
| **CoinGecko (Energy commodities)** | Alternative commodity pricing | Free | 5 min | 🟢 NICE-TO-HAVE |
| **World Bank Data API** | Macroeconomic context | Free | 10 min | 🟢 NICE-TO-HAVE |

### For Geospatial (Optional)

| API | Purpose | Free Tier | Setup Time | Priority |
|-----|---------|-----------|---|---|
| **Google Maps / HERE Maps** | Logistics route mapping | Limited free | 10 min | 🟢 OPTIONAL |

---

## 4. STEP-BY-STEP API KEY ACQUISITION

### A. LLM APIs (Choose One)

**Option 1: Claude (Recommended)**
```bash
# 1. Go to https://console.anthropic.com/
# 2. Sign up for account
# 3. Create API key
# 4. Add to .env:
ANTHROPIC_API_KEY=sk-ant-v0-xxxxx

# Cost: $0.003/1K tokens (input), $0.015/1K tokens (output)
# 20-day budget: ~$50-100 (conservative)
```

**Option 2: OpenAI (GPT-4)**
```bash
# 1. Go to https://platform.openai.com/
# 2. Create account, add billing
# 3. Create API key
# 4. Add to .env:
OPENAI_API_KEY=sk-proj-xxxxx

# Cost: $0.03/1K tokens (input), $0.06/1K tokens (output)
# 20-day budget: ~$100-150
```

### B. News API
```bash
# 1. Go to https://newsapi.org/
# 2. Sign up (free tier: 100 requests/day)
# 3. Copy API key
# 4. Add to .env:
NEWSAPI_KEY=xxxxx

# Free tier is sufficient for prototyping
# Rate limit: 100 requests/day
```

### C. Yahoo Finance (No Key Required)
```bash
# Library: yfinance (Python)
# Install: pip install yfinance
# No API key needed!
# Example:
import yfinance as yf
brent = yf.Ticker("BZ=F").history(period="1y")
```

### D. MarineTraffic AIS Data
```bash
# Option 1: MarineTraffic API (paid, ~$200/mo)
# https://www.marinetraffic.com/en/services/api
# Not feasible for hackathon

# Option 2: Open-Source AIS Data (Free)
# Use: https://www.vesseltracker.com/ (free, limited)
# OR: Download historical AIS CSV from:
# https://marinecadastre.gov/ais/ (US government, free)
# For Hormuz: Use news reports + manual vessel tracking

# Recommendation: Skip live AIS in MVP
# Describe architecture; use news-based vessel tracking
```

### E. OFAC Sanctions
```bash
# 1. Go to https://sanctionslist.ofac.treasury.gov/
# 2. Download CSV (no API key needed)
# 3. Load into database
# 4. No key required!

# Format: Name, ID, Address, Type, Program
```

---

## 5. DATASETS & DATA SOURCES

### A. Free, Public Datasets

| Dataset | Source | Format | Size | Use Case |
|---------|--------|--------|------|----------|
| **MITRE ATT&CK + Geopolitical Data** | News articles (historical) | CSV/JSON | 1-10GB | Historical disruption patterns |
| **IEA Global Energy Outlook** | https://www.iea.org/reports | PDF/CSV | 100MB | Demand forecasts, policy context |
| **OPEC Reference Basket** | https://www.opec.org/ | CSV | 5MB | Historical crude prices |
| **World Bank Commodity Prices** | https://www.worldbank.org/en/research/ | CSV | 10MB | Historical commodity trends |
| **RBI Data (India reserves, imports)** | https://www.rbi.org.in/ | PDF/CSV | 50MB | Strategic Petroleum Reserve data |
| **USGS Energy Statistics** | https://www.usgs.gov/ | CSV | 100MB | Global production data |
| **GIS Shipping Routes** | Natural Earth Data | GeoJSON | 50MB | Strait geometry (Hormuz, Malacca) |

### B. Real-Time Data You'll Mock

| Data | Real Source | MVP Approach | Mock Data |
|------|---|---|---|
| **Current AIS vessel flows** | MarineTraffic API ($200/mo) | Not feasible | Use news reports + manual Hormuz tracker |
| **Live commodity prices** | Brent futures API | Use yfinance (free) | Historical + simulated shock scenarios |
| **News streams** | NewsAPI (100/day free) | Use it directly | Or scrape 500 historical articles |
| **Sanctions updates** | OFAC registry | Download CSV once/week | Historical snapshot sufficient |

### C. Synthetic Data for Scenario Testing

**Create these yourself for demo:**

```python
# Example: Hormuz closure scenario
scenarios = {
    "hormuz_closure_30_percent": {
        "shipping_reduction": 0.30,
        "duration_days": 30,
        "refinery_impact": -0.15,
        "price_spike": 1.25,
        "spr_drain_days": 12
    },
    "iran_sanctions_escalation": {
        "iran_supply_lost": 0.80,
        "alternative_delay": 14,
        "spot_premium": 1.35,
        "supply_gap_days": 5
    }
}
```

---

## 6. ARCHITECTURE OVERVIEW

### System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (User Interface)                    │
│  Dashboard | Risk Scorer | Scenario Modeller | Recommendations     │
└─────────────────────────────────────────────────────────────────────┘
                                  ↕ (API calls)
┌─────────────────────────────────────────────────────────────────────┐
│                        BACKEND (AI & Logic)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [1] Signal Ingestion Layer                                         │
│      ├─ News API → Extract geopolitical signals                    │
│      ├─ Yahoo Finance → Commodity price trends                     │
│      ├─ OFAC Registry → Sanctions changes                          │
│      └─ Manual AIS → Hormuz vessel flows                           │
│                                                                      │
│  [2] Intelligence Layer (Multi-Agent System)                        │
│      ├─ Signal Processor Agent                                      │
│      │   └─ LLM: Extract disruption probabilities from news       │
│      ├─ Risk Scorer Agent                                           │
│      │   └─ LLM: Compute corridor risk (Hormuz, Malacca, etc)     │
│      ├─ Scenario Modeller Agent                                     │
│      │   └─ LLM: "If Hormuz closes, refinery runs drop X%"        │
│      └─ Procurement Recommender Agent                               │
│          └─ LLM: "Pivot X barrels to Russia, Y to Brazil"         │
│                                                                      │
│  [3] Knowledge Base (RAG)                                           │
│      ├─ MITRE ATT&CK-style event precedents                        │
│      ├─ Historical supply shocks + outcomes                        │
│      ├─ Supplier reliability profiles                              │
│      └─ Regulatory constraints                                     │
│                                                                      │
│  [4] Output Engine                                                   │
│      ├─ Real-time risk dashboard                                    │
│      ├─ Scenario impact forecasts                                   │
│      └─ Procurement recommendations + confidence                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                                  ↕ (Database)
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA LAYER (Storage)                         │
│  PostgreSQL | Redis (cache) | Vector DB (embeddings)               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. DISTINCT PROMPTS (Backend vs Frontend)

### BACKEND PROMPTS

#### 7.1 Master Context Prompt (For LLM Backbone)

```markdown
You are an AI energy supply chain resilience analyst for India. Your role is to:
1. Analyze geopolitical & logistics disruption signals
2. Model cascade impacts on energy supplies
3. Recommend adaptive procurement strategies

## Context
- India imports 88% of crude oil
- 40-45% transits through Strait of Hormuz (single-point-of-failure risk)
- Strategic Petroleum Reserves = 9.5 days of national consumption
- Current real-time signals: [INJECTED FROM NEWS/AIS/SANCTIONS]

## Your Analysis Framework
1. SIGNAL DETECTION: Identify disruption events in news/data
2. RISK SCORING: Quantify probability × impact for each corridor
3. SCENARIO MODELING: Project 30-90 day outcomes under disruption
4. PROCUREMENT OPTIMIZATION: Recommend source/route mix changes

## Response Format
Always provide:
- Risk assessment (0-100 scale)
- Confidence level (high/medium/low)
- Supporting evidence (with sources)
- Time horizon (hours to impact)
- Recommended actions (specific, executable)

## Constraints
- Be conservative: False negatives (missed risks) are worse than false positives
- Quantify impact: "Brent crude +$X/barrel, GDP impact -X%"
- Consider delays: Alternative sourcing takes 10-14 days
- Flag geopolitical assumptions explicitly
```

#### 7.2 Signal Extraction Prompt (News → Risk Signals)

```markdown
You are a geopolitical signal extraction agent. Analyze the following news article 
for energy supply disruption signals.

ARTICLE:
[INSERT NEWS TEXT]

ANALYZE:
1. What disruption event is described? (e.g., Houthi attack, sanctions, war)
2. Which corridor is affected? (Hormuz, Red Sea, Suez, Russia-Europe, etc.)
3. What is the disruption probability? (%)
4. What is the likely duration? (hours/days/weeks)
5. Historical precedent? (e.g., "Similar to 2022 Yemen attacks")
6. Confidence in interpretation? (high/medium/low)

OUTPUT FORMAT (JSON):
{
  "event": "...",
  "corridor": "...",
  "probability": 0-100,
  "duration_days": N,
  "precedent": "...",
  "confidence": "high/medium/low",
  "summary": "..."
}
```

#### 7.3 Risk Scorer Prompt (Probability × Impact)

```markdown
You are an energy supply chain risk analyst. Calculate disruption risk for India's crude 
oil corridors using current market conditions and geopolitical context.

INPUTS:
- Current Hormuz flow: {CURRENT_FLOW_BBL/DAY}
- Current Brent price: ${CURRENT_PRICE}/barrel
- SPR drawdown rate (if disrupted): {RATE}% per day
- Days of reserve remaining: {SPR_DAYS}

DISRUPTION SCENARIOS:
1. Hormuz partial closure (30%)
2. Full Hormuz closure (100%)
3. Iran sanctions escalation
4. Red Sea shipping suspension
5. OPEC+ production cut

FOR EACH SCENARIO:
- Probability of occurrence (%) in next 30/90 days
- Impact on India's oil availability (% reduction)
- Price impact (multiplier, e.g., 1.25x = +25%)
- Days to SPR exhaustion
- Time to source alternatives

CONFIDENCE SCORING:
- High: Geopolitical threat is immediate/documented
- Medium: Plausible but escalation uncertain
- Low: Speculative based on historical patterns

OUTPUT: Risk matrix (scenario × probability × impact)
```

#### 7.4 Scenario Modeller Prompt

```markdown
You are an energy economist. Model the cascading impact of this disruption on India:

DISRUPTION: {SCENARIO}
DURATION: {DAYS}
SUPPLY LOSS: {PERCENT}% of current imports

CALCULATE (with assumptions explicit):
1. Daily crude shortage (barrels)
2. SPR drawdown acceleration
3. Days until SPR critical (5-day reserve)
4. Refinery run-rate impact
5. Domestic fuel price increase
6. Power sector stress (coal → fuel switch)
7. GDP trajectory impact (if sustained)
8. Ripple effects (inflation, transport costs)

OUTPUT FORMAT:
Timeline: Day 1, Day 5, Day 10, Day 30
├─ Supply gap: X barrels
├─ SPR reserve remaining: Y days
├─ Fuel price: $Z/liter
├─ Power outages risk: HIGH/MEDIUM/LOW
└─ Economic impact: -X% GDP growth (annualized)

## ASSUMPTIONS TO DOCUMENT:
- Refinery capacity: [assume 250M tonnes/year]
- Demand elasticity: [assume inelastic short-term]
- Alternative sourcing delay: [assume 10-14 days]
- Strategic reserve drawdown speed: [assume max speed]
```

#### 7.5 Procurement Recommender Prompt

```markdown
You are a crude oil procurement strategist for India's energy ministry. Given the 
disruption scenario below, recommend adaptive procurement strategy.

CURRENT PORTFOLIO:
- Saudi Arabia: 40% of imports
- Iraq: 20%
- Iran: 8% (under sanctions, unreliable)
- Russia: 10%
- Brazil: 5%
- Others: 17%

DISRUPTION: {SCENARIO}
SUPPLY GAP: {VOLUME_BBL/DAY}
TIME TO ALTERNATE SOURCE: 10-14 days
BUDGET CONSTRAINT: None (emergency mode)

RECOMMEND:
1. Which sources to increase? (by % of current)
2. Which routes to prioritize? (Malacca, Suez, direct)
3. Spot market actions? (volume, price ceiling)
4. SPR drawdown schedule? (daily rate)
5. Demand-side measures? (rationing, switch to coal)
6. Negotiation talking points? (for supplier governments)

FOR EACH RECOMMENDATION:
- Implementation timeline (hours/days)
- Volume impact (barrels/day)
- Cost increase ($/barrel premium)
- Delivery reliability (%)
- Geopolitical risk (if applicable)

CONFIDENCE & CAVEATS:
- Acknowledge supplier constraints
- Flag geopolitical escalation risks
- Quantify uncertainty ranges
```

---

### FRONTEND PROMPTS

#### 7.6 Dashboard Narrative Prompt (For LLM-Generated Insights)

```markdown
You are a data journalist writing executive briefs for the Energy Ministry dashboard. 
Generate clear, actionable insight cards from supply chain intelligence.

DATA INPUTS:
- Current risk score: {SCORE}/100
- Primary threats: {THREATS}
- Recommended actions: {ACTIONS}
- Confidence: {CONFIDENCE}

GENERATE (per card, max 150 chars):
1. HEADLINE: Urgent, specific, quantified
   Example: "Hormuz Risk +35% amid Houthi escalation → 8-day SPR depletion"

2. INSIGHT: Why it matters in one sentence
   Example: "If Red Sea remains blocked, alternative sourcing delay exceeds reserve buffer"

3. CALL-TO-ACTION: One concrete step
   Example: "Activate long-term contracts with Brazil (delivery in 12 days)"

4. CONFIDENCE: Transparent uncertainty
   Example: "Medium confidence: Houthi capabilities growing, but escalation speed unclear"

TONE:
- Clear, not alarmist
- Quantified, not vague
- Actionable, not analytical
- Honest about uncertainty
```

#### 7.7 Scenario Comparison Prompt (For Visualization)

```markdown
You are an analyst creating comparison cards for energy supply scenarios.

SCENARIOS TO COMPARE:
1. Base case (no disruption)
2. Moderate (e.g., Hormuz 30% closure)
3. Severe (e.g., Hormuz 100% closure, Iran sanctions)

FOR EACH SCENARIO, GENERATE:
- Timeframe to SPR critical (days)
- Recommended procurement pivot (% changes by source)
- Cost impact (additional $/barrel over 90 days)
- Probability in next 90 days (%)
- Recommended response actions (list of 3-5)

FORMAT: Comparison table + narrative explanation
```

---

## 8. BACKEND ARCHITECTURE & SETUP

### Tech Stack

```yaml
Language: Python 3.10+
Framework: FastAPI (REST API) + LangChain (agentic orchestration)
LLM: Claude (via Anthropic API)
Database: PostgreSQL + Redis
Vector DB: Weaviate or Pinecone (for RAG)
Data Processing: Pandas, NumPy
External APIs: NewsAPI, yfinance, OFAC

Python Packages:
- fastapi, uvicorn (API framework)
- langchain, langsmith (agentic AI)
- anthropic (Claude API)
- sqlalchemy (ORM)
- pydantic (data validation)
- httpx, aiohttp (async HTTP)
- yfinance, newsapi (external APIs)
- pandas, numpy (data processing)
- pydantic-settings (config management)
```

### Backend Directory Structure

```
energy-guard/
├── backend/
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Environment config (.env)
│   ├── requirements.txt         # Python dependencies
│   │
│   ├── agents/                 # Multi-agent system
│   │   ├── __init__.py
│   │   ├── signal_processor.py    # News → risk signals
│   │   ├── risk_scorer.py         # Corridor risk calculation
│   │   ├── scenario_modeller.py   # Impact forecasting
│   │   └── recommender.py         # Procurement suggestions
│   │
│   ├── data/                   # Data ingestion & processing
│   │   ├── __init__.py
│   │   ├── news_ingestion.py      # NewsAPI client
│   │   ├── market_data.py         # yfinance + commodity prices
│   │   ├── sanctions_loader.py    # OFAC registry
│   │   ├── ais_tracker.py         # Manual Hormuz tracking
│   │   └── processor.py           # Data cleaning & enrichment
│   │
│   ├── db/                     # Database & storage
│   │   ├── __init__.py
│   │   ├── models.py              # SQLAlchemy models
│   │   ├── session.py             # DB connection manager
│   │   └── migrations/
│   │
│   ├── rag/                    # Knowledge base & retrieval
│   │   ├── __init__.py
│   │   ├── vector_store.py        # Weaviate/Pinecone integration
│   │   ├── knowledge_base.py      # Historical disruptions + precedents
│   │   └── retriever.py           # RAG query engine
│   │
│   ├── api/                    # REST endpoints
│   │   ├── __init__.py
│   │   ├── routes.py              # /risk, /scenario, /recommend
│   │   └── schemas.py             # Pydantic schemas (request/response)
│   │
│   ├── orchestration/          # Agent coordination
│   │   ├── __init__.py
│   │   ├── workflow.py            # Multi-agent orchestrator
│   │   └── state_manager.py       # State persistence
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       └── helpers.py

├── frontend/                   # React frontend (see section 9)

├── .env.example               # Environment template
├── docker-compose.yml          # PostgreSQL + Redis services
└── README.md
```

### Backend Configuration (.env)

```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-v0-xxxxx
NEWSAPI_KEY=xxxxx

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/energy_guard
REDIS_URL=redis://localhost:6379

# Vector DB
WEAVIATE_URL=http://localhost:8080
# OR
PINECONE_API_KEY=xxxxx
PINECONE_ENVIRONMENT=gcp-starter

# API Config
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
FASTAPI_ENV=development

# LLM Config
LLM_MODEL=claude-3-sonnet-20240229
LLM_MAX_TOKENS=2000
LLM_TEMPERATURE=0.7
```

---

## 9. FRONTEND ARCHITECTURE & SETUP

### Tech Stack

```yaml
Framework: React 18 + TypeScript
UI Library: shadcn/ui or Material-UI
State: TanStack Query (data fetching) + Zustand (state)
Visualization: Recharts or Plotly.js
Maps: Mapbox GL or Leaflet (optional)
Styling: Tailwind CSS
API Client: Axios
```

### Frontend Directory Structure

```
frontend/
├── src/
│   ├── main.tsx                    # Entry point
│   ├── App.tsx                     # Root component
│   │
│   ├── pages/
│   │   ├── Dashboard.tsx           # Main overview
│   │   ├── RiskAnalysis.tsx        # Risk scorer interface
│   │   ├── ScenarioModeller.tsx    # Scenario builder
│   │   ├── Recommendations.tsx     # Procurement suggestions
│   │   └── HistoricalData.tsx      # Historical trends
│   │
│   ├── components/
│   │   ├── RiskScoreCard.tsx       # Risk display (0-100)
│   │   ├── CorridorMap.tsx         # Hormuz + routes visualization
│   │   ├── ScenarioComparison.tsx  # Side-by-side scenarios
│   │   ├── TimelineChart.tsx       # 30-90 day forecast
│   │   ├── RecommendationCard.tsx  # Action cards
│   │   └── common/
│   │       ├── Header.tsx
│   │       ├── Navigation.tsx
│   │       └── Footer.tsx
│   │
│   ├── hooks/
│   │   ├── useRiskScore.ts         # Fetch risk data
│   │   ├── useScenarios.ts         # Fetch scenario results
│   │   └── useRecommendations.ts   # Fetch actions
│   │
│   ├── services/
│   │   ├── api.ts                  # Axios client
│   │   ├── riskService.ts          # Risk API calls
│   │   └── scenarioService.ts      # Scenario API calls
│   │
│   ├── store/
│   │   ├── useAppStore.ts          # Global state (Zustand)
│   │   └── useUIStore.ts           # UI state
│   │
│   ├── types/
│   │   ├── index.ts                # TypeScript interfaces
│   │   └── api.ts                  # API response types
│   │
│   └── styles/
│       └── globals.css             # Tailwind + custom
│
├── public/
│   ├── index.html
│   └── assets/
│
├── .env.example
├── tsconfig.json
├── vite.config.ts
└── package.json
```

### Frontend Configuration (.env)

```bash
# .env file
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
VITE_APP_TITLE=EnergyGuard
VITE_APP_VERSION=0.1.0
```

---

## 10. APPROACH & SOLUTIONIZATION

### Problem Decomposition

```
CHALLENGE: India's energy supply chain is vulnerable to geopolitical shocks
├─ DIMENSION 1: Detection (What disruptions are happening?)
│  └─ Solution: Multi-source signal aggregation (news + AIS + sanctions)
│
├─ DIMENSION 2: Prediction (What will happen if disruption occurs?)
│  └─ Solution: Scenario modelling + impact forecasting (LLM reasoning)
│
├─ DIMENSION 3: Response (What actions should we take?)
│  └─ Solution: Procurement optimization (agentic recommendation)
│
└─ DIMENSION 4: Execution (How do we make decisions fast?)
   └─ Solution: Real-time dashboard + confidence scoring
```

### Solution Architecture (Why This Approach)

#### Phase 1: Intelligence Ingestion (Days 1-5)

**Goal:** Aggregate real-time disruption signals from multiple sources

**Approach:**
- NewsAPI → Extract geopolitical events (Houthi attacks, sanctions, wars)
- Yahoo Finance → Track commodity price spikes (early warning)
- OFAC Registry → Monitor new sanctions (policy changes)
- Manual AIS → Track Hormuz vessel flows (shipping patterns)

**Why this works:**
- News is fast (hours of latency)
- Prices are leading indicators (traders react first)
- Sanctions are authoritative (policy is official)
- AIS data is ground truth (physical vessel movement)

**Output:** Structured signal log (time, event, source, confidence)

#### Phase 2: Risk Intelligence (Days 6-12)

**Goal:** Score disruption probability × impact for each corridor

**Approach:**
- Signal Processor Agent: LLM extracts risk signals from unstructured news
- Risk Scorer Agent: LLM calculates corridor vulnerability (Hormuz, Malacca, Suez)
- Knowledge Base (RAG): Historical precedents (2022 Houthi attacks, 1973 embargo)

**Why LLM reasoning:**
- Geopolitical analysis is qualitative (news sentiment + escalation patterns)
- Requires contextual understanding (What does "escalation" mean?)
- Combines multiple signals (Houthi attacks + US statements + price moves)
- Explains reasoning (judges want transparency)

**Output:** Risk matrix (30 scenarios × probability × impact)

#### Phase 3: Scenario Modelling (Days 13-16)

**Goal:** Project 30-90 day impacts (supply, price, reserves, economy)

**Approach:**
- Scenario Modeller Agent: LLM models causal chains
  - "If Hormuz closes 30% → India loses X barrels/day → SPR drains in 14 days"
- Uses explicit assumptions (refinery capacity, demand elasticity, alternative delays)
- Produces quantified impact (GDP, fuel prices, power outages)

**Why agent-based:**
- Scenarios are conditional reasoning ("If X, then Y")
- Requires domain logic (refinery runs, supply dynamics)
- Needs transparency (show all assumptions)

**Output:** Time-series forecasts (Day 1, 5, 10, 30)

#### Phase 4: Procurement Optimization (Days 17-19)

**Goal:** Recommend adaptive sourcing strategies

**Approach:**
- Recommender Agent: LLM generates portfolio adjustments
  - "Increase Russia supply 300K bbl/day (delivery in 12 days)"
  - "Reduce Iran reliance (already sanctioned, unreliable)"
  - "Activate spot market for 500K bbl/day"
- Scores recommendations (timeline, cost, geopolitical risk)

**Why agent-based:**
- Optimization is multi-objective (volume × cost × reliability × time)
- Requires domain knowledge (supplier constraints, geopolitical risks)
- Needs explainability (why this portfolio, not that one?)

**Output:** Actionable recommendations (specific, prioritized, timed)

#### Phase 5: User Interface (Days 17-20)

**Goal:** Make intelligence accessible to decision-makers in real time

**Approach:**
- Risk Dashboard: Current risk score (0-100) + top threats
- Scenario Explorer: Compare 3-5 disruption scenarios
- Timeline View: 30-90 day impact forecast
- Recommendation Cards: Procurement actions + confidence
- Evidence Layer: Click through to news sources, data

**Why this design:**
- Executives need quick risk at a glance (risk score card)
- Decision-makers need scenario comparison (what if X?)
- Procurement teams need specific actions (what to do)
- Auditors need evidence (traceability)

**Output:** Interactive web app (mobile-friendly)

---

## 11. MASTER CONTEXT PROMPT (For Any LLM Collaborator)

Save this prompt to onboard any AI model (Claude, ChatGPT, Llama) to the project:

```markdown
# EnergyGuard: Master Context Prompt

## Project Overview
You are an AI engineer building EnergyGuard, an energy supply chain resilience system for India.

**Problem:** India imports 88% of crude oil. 40-45% flows through Hormuz (single-point-of-failure).
**Solution:** Real-time disruption forecasting + adaptive procurement recommendations.
**Timeline:** 20 days (solo development, July 2-22, 2026).
**Scope:** MVP covering signal detection → risk scoring → scenario modeling → procurement recommendations.

---

## Architecture (Layers)

### Input Layer
- News feeds (geopolitical signals via NewsAPI)
- Commodity markets (Brent crude prices via yfinance)
- Sanctions registries (OFAC, Iran pressure)
- AIS tracking (Hormuz vessel flows, manual)

### Intelligence Layer (Multi-Agent LLM System)
- **Signal Processor:** Extracts risk events from unstructured news
- **Risk Scorer:** Calculates corridor vulnerability (0-100 scale)
- **Scenario Modeller:** Projects 30-90 day supply/price/reserve impacts
- **Recommender:** Suggests procurement strategy adjustments

### Knowledge Base (RAG)
- Historical disruptions (2022 Yemen, 1973 embargo, etc.)
- Supplier reliability profiles
- Regulatory constraints
- Geopolitical precedents

### Output Layer
- Real-time risk dashboard
- Scenario comparison interface
- Procurement recommendations + confidence
- Evidence traceability (links to news sources)

---

## Key Concepts

### Risk Scoring (0-100)
- 0-20: Low (routine operations, no disruption signals)
- 20-40: Moderate (watchful, some geopolitical tension)
- 40-60: High (active disruption events, need contingency planning)
- 60-80: Very High (imminent supply impact, activate alternatives)
- 80-100: Critical (supply crisis, emergency measures)

### Corridors of Interest
1. **Hormuz Strait** (40-45% of Indian imports)
   - Chokepoint: 34 km wide
   - Risk factors: US-Iran tensions, Houthi attacks, tanker seizures
   
2. **Red Sea** (alternative shipping route from Africa/Europe)
   - Risk factors: Houthi attacks, piracy, shipping delays
   
3. **Suez Canal** (Egypt transit)
   - Risk factors: Political instability, terrorism, closure risks
   
4. **Malacca Strait** (alternate shipping from Russia/SE Asia)
   - Risk factors: Piracy, geopolitics, congestion
   
5. **Land/Rail Routes** (Russia, Central Asia)
   - Risk factors: Sanctions, logistics complexity, weather

### Disruption Scenarios (Test Cases)
1. **Hormuz Partial Closure (30%):** Houthi attacks intensify
2. **Hormuz Full Closure (100%):** US-Iran military escalation
3. **Iran Sanctions Escalation:** US pressure forces halt
4. **Red Sea Shipping Block:** Regional conflict expands
5. **OPEC+ Cut:** Geopolitical coordination (Russia-Saudi pressure)

### Impact Metrics
- **Supply Gap:** Barrels/day lost
- **SPR Burn Rate:** Days of reserves if disruption sustained
- **Price Spike:** Brent crude multiplier (e.g., 1.35x = +35%)
- **Refinery Impact:** Run-rate reduction (%)
- **GDP Impact:** Annualized growth reduction (%)
- **Geopolitical Risk:** Escalation probability (%)

---

## Development Priorities (MVP Scope)

### Must-Have (By July 22)
✅ Signal ingestion pipeline (news + prices + sanctions)
✅ Risk scorer (corridor vulnerability 0-100)
✅ Scenario modeller (3-5 major disruption cases)
✅ Procurement recommender (top 3-5 actions per scenario)
✅ Dashboard (risk card + scenario comparison + recommendations)
✅ Working demo (video showing end-to-end flow)

### Nice-to-Have (If time permits)
- Live AIS vessel tracking (Hormuz flows)
- Full energy economist modeling (GDP cascades)
- Multi-language support for government use
- Mobile optimization

### Explicitly Out-of-Scope
- Real-time market trading signals
- Detailed refinery simulation (use simplified models)
- Autonomous action execution (recommendations only, humans decide)
- Classified intelligence integration (public data only)

---

## LLM Best Practices (For Agents)

### Prompting Strategy
1. **Be explicit about role:** "You are a geopolitical risk analyst"
2. **Provide context:** "Current Hormuz risk is 45%, Brent is $95/barrel"
3. **Demand structure:** Always request JSON output with specific fields
4. **Ask for confidence:** "Rate your confidence (high/medium/low)"
5. **Require citations:** "Cite news sources for all claims"

### Output Validation
- Responses must include uncertainty quantification ("X% probability, confidence: medium")
- All probability claims must be traceable to sources
- Recommendations must include timeline + cost estimates
- No hallucinated data (prefer "insufficient data" to guessing)

### Error Handling
- If model refuses to respond: Fall back to historical averages
- If confidence is "low": Flag as uncertain, present ranges
- If data is missing: Use synthetic/mock data, clearly label
- If escalation risk is high: Alert user immediately

---

## Data Dictionary

### Risk Object
```json
{
  "corridor": "Hormuz",
  "probability_percent": 65,
  "impact_percent": 35,
  "composite_risk_0_100": 72,
  "confidence": "medium",
  "sources": ["NewsAPI: Houthi attack report", "MarineTraffic: vessel tracking"],
  "timestamp": "2026-07-15T14:30:00Z"
}
```

### Scenario Object
```json
{
  "scenario_name": "Hormuz Partial Closure (30%)",
  "disruption_type": "shipping_reduction",
  "duration_days": 30,
  "probability_percent": 35,
  "impact_timeline": {
    "day_1": {"supply_gap_bbl": 500000, "spr_drain_days": 18},
    "day_5": {"supply_gap_bbl": 500000, "spr_drain_days": 14},
    "day_10": {"supply_gap_bbl": 300000, "spr_drain_days": 20},
    "day_30": {"supply_gap_bbl": 0, "spr_drain_days": 30}
  },
  "price_impact": 1.25,
  "refinery_impact_percent": -15,
  "gdp_impact_percent": -0.5
}
```

### Recommendation Object
```json
{
  "scenario": "Hormuz Partial Closure (30%)",
  "recommendations": [
    {
      "priority": 1,
      "action": "Increase Russia crude imports by 300K bbl/day",
      "timeline_days": 12,
      "volume_bbl": 300000,
      "cost_premium_dollars_per_barrel": 2.50,
      "geopolitical_risk": "medium",
      "confidence": "high"
    },
    {
      "priority": 2,
      "action": "Activate spot market for 500K bbl/day",
      "timeline_days": 3,
      "volume_bbl": 500000,
      "cost_premium_dollars_per_barrel": 5.00,
      "geopolitical_risk": "low",
      "confidence": "high"
    }
  ]
}
```

---

## Evaluation Criteria (For Judging)

The judges will assess EnergyGuard on:

1. **Innovation (25%):** Novel approach to energy supply chain risk
   - Multi-agent agentic AI + RAG is novel
   - Real-time signal fusion is new
   - Scenario modeling with LLM reasoning is sophisticated
   
2. **Business Impact (25%):** Solves a real, pressing problem
   - India's energy security is critical
   - Prevents multi-billion rupee supply shocks
   - Addresses gap in current tools
   
3. **Technical Excellence (20%):** Implementation quality
   - Signal detection lead time (how early do you warn?)
   - Scenario model fidelity (do assumptions match reality?)
   - Recommendation quality (are actions feasible + impactful?)
   
4. **Scalability (15%):** Can this work for other scenarios?
   - Does it work for other import-dependent countries?
   - Can it scale to other supply chains (food, semiconductors)?
   - Architecture extensible to new data sources?
   
5. **User Experience (15%):** Can decision-makers actually use it?
   - Dashboard clarity (is risk obvious at a glance?)
   - Recommendation actionability (can a procurement officer follow them?)
   - Confidence transparency (do users understand uncertainty?)

---

## Debugging & Support

### Common Issues & Solutions

**Issue:** "NewsAPI returns vague articles, hard to extract signals"
**Solution:** Use LLM to interpret news, ask for explicit probability + timeline

**Issue:** "Scenario modeling produces unrealistic numbers"
**Solution:** Add constraint checks (refinery max capacity, SPR max drawdown rate)

**Issue:** "Recommendations seem generic/obvious"
**Solution:** Add geopolitical context (which suppliers are sanctioned? which are reliable?)

**Issue:** "Risk score doesn't change even when news escalates"
**Solution:** Increase LLM temperature slightly, ensure news is recent (< 24 hrs)

---

## Success Criteria (MVP Definition)

By July 22, the MVP must demonstrate:
1. ✅ Real-time risk score (updates as news/prices change)
2. ✅ 3-5 scenario forecasts (with explicit assumptions)
3. ✅ 5-10 procurement recommendations (with timelines + costs)
4. ✅ Working web dashboard (risk card + scenarios + recommendations)
5. ✅ Evidence layer (click through to source data)
6. ✅ Demo video (3-5 min showing end-to-end flow)

---

## Questions to Ask When Stuck

1. "Is this signal (news/price spike) real or noise?"
   → Use LLM confidence scoring + multiple sources
   
2. "What happens if scenario X extends beyond 30 days?"
   → Model multiple durations, show uncertainty ranges
   
3. "How do I explain this recommendation to a skeptical procurement officer?"
   → Show cost-benefit + risk comparison vs. alternatives
   
4. "Is my risk score calibrated correctly?"
   → Compare to historical events (Hormuz 2019, Yemen 2022)
   
5. "What happens if all my assumptions are wrong?"
   → Run sensitivity analysis, show which assumptions matter most

---

## Resources & References

### India Energy Context
- RBI Strategic Petroleum Reserve levels: https://www.rbi.org.in/
- IEA India Energy Outlook: https://www.iea.org/
- NITI Aayog energy strategy: https://www.niti.gov.in/

### Geopolitical Risk
- ACLED (armed conflict data): https://www.acleddata.com/
- Reuters alerts: https://www.reuters.com/
- CNN Breaking News: https://www.cnn.com/

### Energy Markets
- EIA (US Energy Info Admin): https://www.eia.gov/
- OPEC: https://www.opec.org/
- BP Statistical Review: https://www.bp.com/

### Maritime/Logistics
- IMO (International Maritime Org): https://www.imo.org/
- Lloyd's List: https://lloydslist.maritime.com/
- Project cargo data: https://www.projectcargo.com.br/

---

## Contact & Collaboration

If you're implementing a component, please:
1. Document your assumptions explicitly
2. Provide test data (even if synthetic)
3. Show confidence levels in outputs
4. Include error cases in testing
5. Flag any data access bottlenecks

---

**Last Updated:** July 2, 2026
**Version:** 1.0 (MVP)
**Maintained By:** [Your Name]
```

---

## 12. QUICK START CHECKLIST (First 48 Hours)

### Day 1 (July 2 - Setup)

```bash
# 1. Environment & APIs
- [ ] Clone repo structure
- [ ] Create .env with keys (NewsAPI, OpenAI/Anthropic, yfinance)
- [ ] Test API connectivity (news, prices, yfinance)

# 2. Backend scaffolding
- [ ] FastAPI app initialized
- [ ] Models defined (Risk, Scenario, Recommendation)
- [ ] Database tables created
- [ ] Redis cache configured

# 3. Frontend scaffolding
- [ ] React app initialized (Vite + TypeScript)
- [ ] Basic layout (header, navigation, main content)
- [ ] API client configured

# 4. Knowledge base
- [ ] Historical disruptions CSV loaded
- [ ] OFAC sanctions CSV imported
- [ ] Vector DB initialized (if using RAG)
```

### Day 2 (July 3 - First Agent)

```bash
# Build Signal Processor Agent
- [ ] NewsAPI integration working
- [ ] LLM prompt for signal extraction tested
- [ ] Sample output: JSON with [event, corridor, probability, confidence]

# Test with real example:
- [ ] "Houthi attacks Red Sea shipping" → Extracts risk signal ✓
- [ ] "Brent crude +8% on Iran tensions" → Identifies geopolitical signal ✓
```

---

## 13. ENHANCEMENT PROMPTS (For Later Iterations)

### Enhancement 1: Geopolitical Escalation Detector

```markdown
You are a geopolitical analyst. Given a series of news events over the past 7 days,
assess the escalation trajectory for energy supply disruption.

EVENTS:
{LIST OF NEWS ITEMS WITH DATES}

ANALYZE:
1. Is tension escalating (trajectory) or de-escalating?
2. What is the critical trigger for military action? (if any)
3. Historical precedent for this escalation pattern?
4. What statement/action would reverse the trend?
5. Probability of military action in next 7/14/30 days?

OUTPUT: Escalation score (1-10) + timeline to potential action
```

### Enhancement 2: Supply Chain Resilience Score

```markdown
You are an energy security officer. Rate India's crude oil supply chain resilience
against the current disruption scenario.

CURRENT PORTFOLIO:
- Saudi: 40%, Iraq: 20%, Russia: 10%, Brazil: 5%, Iran: 8%, Others: 17%
- SPR reserve: 9.5 days
- Refinery capacity: 250M tonnes/year

SCENARIO:
{DISRUPTION DETAILS}

RESILIENCE ASSESSMENT:
1. Vulnerability ranking (1-10)
2. Critical dependencies (which suppliers matter most?)
3. Time to critical reserve level
4. Recovery time if disruption reverses
5. Recommendations to improve resilience

OUTPUT: Resilience Score (1-10) + mitigation priorities
```

### Enhancement 3: Geospatial Risk Visualization

```markdown
You are a GIS analyst. Create a risk heat map description for India's crude oil supply routes.

INPUTS:
- Current risk scores by corridor (Hormuz, Red Sea, Suez, Malacca)
- Vessel tracking data (if available)
- Infrastructure locations (refineries, SPR depots, ports)

GENERATE:
1. Which regions should be highlighted as HIGH RISK?
2. Which trade routes are most vulnerable?
3. Where should contingency infrastructure be located?
4. How should patrol/protection be distributed?

OUTPUT: GIS layer description (latitude/longitude, risk zones)
```

### Enhancement 4: Multi-Country Comparison

```markdown
You are a comparative energy security analyst. Compare energy supply chain resilience
across countries similar to India.

COUNTRIES TO COMPARE:
- India (88% crude import, Hormuz-dependent)
- Japan (95% crude import, Hormuz-dependent)
- South Korea (92% crude import, Hormuz-dependent)
- Turkey (80% crude import, Russia-dependent)

FOR EACH:
1. Vulnerability profile (chokepoints, dependencies)
2. Resilience strategies (SPR, diversification, alternatives)
3. Response protocols (government + industry coordination)
4. Effectiveness of strategies (if tested)

OUTPUT: Comparison matrix + lessons for India
```

---

## Summary

You now have:
- ✅ Project naming + GitHub description
- ✅ Complete API key list + acquisition guide
- ✅ Datasets & data sources (all public)
- ✅ Backend architecture (FastAPI + LangChain + multi-agent)
- ✅ Frontend architecture (React + dashboard components)
- ✅ 5 distinct prompts (backend agents)
- ✅ Master context prompt (for any LLM collaborator)
- ✅ Approach & solutionization framework
- ✅ First 48-hour checklist
- ✅ Enhancement prompts for later

**Next Step:** Start with Day 1 checklist, get one agent working by end of July 3, and iterate forward. Good luck! 🚀
