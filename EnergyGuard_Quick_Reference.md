# EnergyGuard: Quick Reference Card

---

## 🎯 PROJECT AT A GLANCE

| Aspect | Detail |
|--------|--------|
| **Name** | EnergyGuard |
| **GitHub** | `energy-guard` |
| **Pitch** | Real-time energy supply chain resilience for India (88% import dependency) |
| **Stack** | Python (FastAPI) + React + SQLite + Claude LLM |
| **Deadline** | July 22, 2026 (20 days) |
| **Key Focus** | Signal detection → Risk scoring → Scenario modeling → Procurement recommendations |

---

## 🔑 CRITICAL API KEYS (Setup in 30 mins)

### Must-Have

```bash
# 1. Claude API (Backbone)
ANTHROPIC_API_KEY = Get from https://console.anthropic.com/
Budget: ~$50-100 for 20 days
Time to setup: 5 minutes

# 2. NewsAPI (Geopolitical Signals)
NEWSAPI_KEY = Get from https://newsapi.org/
Free tier: 100 requests/day (sufficient for MVP)
Time to setup: 5 minutes

# 3. Yahoo Finance (No Key Needed!)
# Just: pip install yfinance
# Code: import yfinance as yf; brent = yf.Ticker("BZ=F").history()
Time to setup: 2 minutes
```

### Nice-to-Have

```bash
# 4. OFAC Sanctions (No Key, Download CSV)
# https://sanctionslist.ofac.treasury.gov/
Time to setup: 5 minutes

# 5. IEA Data (Freemium)
# https://www.iea.org/reports
Time to setup: 10 minutes (optional)
```

**Total Setup Time: ~30 minutes**

---

## 🏗️ ARCHITECTURE IN ONE PAGE

```
┌────────────────────────────────────────────┐
│         FRONTEND (React Dashboard)         │
│  Risk Score | Scenarios | Recommendations  │
└─────────────┬────────────────────────────┘
              │ (API calls)
┌─────────────▼────────────────────────────────────┐
│ BACKEND (FastAPI + Multi-Agent LLM Orchestration) │
├────────────────────────────────────────────────┤
│ [1] Signal Processor    → News → Risk signals  │
│ [2] Risk Scorer         → Corridor risk 0-100  │
│ [3] Scenario Modeller   → If X, then Y impact  │
│ [4] Recommender         → Buy X barrels from Y  │
└─────────────┬────────────────────────────────────┘
              │ (Data)
┌─────────────▼────────────────────────────────────┐
│ DATA LAYER (SQLite prototype DB)                 │
└────────────────────────────────────────────────┘
```

---

## 📊 5 CORE PROMPTS (Copy-Paste Ready)

### Prompt 1: Signal Extraction (News → Risk)

```markdown
You are a geopolitical risk analyst. Extract supply disruption signals from this news.

NEWS: {INSERT_TEXT}

ANALYZE:
1. Event type? (attack, sanctions, war, etc)
2. Affected corridor? (Hormuz, Red Sea, Suez, Malacca)
3. Probability %? (0-100)
4. Duration? (hours/days/weeks)
5. Confidence? (high/med/low)

OUTPUT JSON:
{"event": "...", "corridor": "...", "probability": N, "duration_days": N, "confidence": "..."}
```

### Prompt 2: Risk Scorer (Vulnerability Calculation)

```markdown
Score India's crude oil corridor risk. Current situation:
- Hormuz flow: 1.5M bbl/day
- Brent price: $95/barrel
- SPR reserve: 9.5 days

SCENARIOS:
1. Hormuz 30% closure (Houthi attacks)
2. Full closure (US-Iran war)
3. Iran sanctions escalation
4. Red Sea shipping block
5. OPEC+ cut

FOR EACH: probability%, impact%, composite risk 0-100
OUTPUT: JSON array of scenarios with scores
```

### Prompt 3: Scenario Modeller (Impact Forecasting)

```markdown
Model this disruption's impact on India over 30 days.

DISRUPTION: {SCENARIO}
SUPPLY LOSS: {PERCENT}%

CALCULATE & SHOW TIMELINE (Day 1, 5, 10, 30):
- Supply gap (barrels)
- SPR drain rate (days remaining)
- Brent price ($/barrel)
- Refinery impact (%)
- Geopolitical escalation risk

DOCUMENT ALL ASSUMPTIONS
```

### Prompt 4: Procurement Recommender (Action Generator)

```markdown
Current portfolio: Saudi 40%, Iraq 20%, Russia 10%, Brazil 5%, Iran 8%, Others 17%
SPR: 9.5 days | Disruption: {SCENARIO} | Gap: {VOLUME}

RECOMMEND:
1. Which sources to increase? (by %)
2. Routes to prioritize?
3. Spot market volume?
4. SPR drawdown schedule?
5. Negotiation talking points?

FOR EACH: timeline, volume impact, cost, geopolitical risk
```

### Prompt 5: Dashboard Narrative (Insight Cards)

```markdown
Generate executive brief cards from this supply chain intelligence:
- Risk score: {SCORE}/100
- Primary threats: {THREATS}
- Recommended actions: {ACTIONS}

PER CARD (max 150 chars):
1. HEADLINE (specific, quantified)
2. INSIGHT (one sentence, why it matters)
3. CTA (concrete action step)
4. CONFIDENCE (transparency about uncertainty)

TONE: Clear, not alarmist. Quantified, not vague.
```

---

## 📁 DIRECTORY STRUCTURE (20 days, solo)

```
energy-guard/
├── backend/
│   ├── agents/
│   │   ├── signal_processor.py      ← NewsAPI → signals
│   │   ├── risk_scorer.py           ← Corridor risk 0-100
│   │   ├── scenario_modeller.py     ← Impact forecasts
│   │   └── recommender.py           ← Procurement suggestions
│   ├── data/
│   │   ├── news_ingestion.py
│   │   ├── market_data.py           ← yfinance (Brent)
│   │   └── sanctions_loader.py      ← OFAC registry
│   ├── api/
│   │   └── routes.py                ← /risk, /scenario, /recommend
│   └── main.py                      ← FastAPI app
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx        ← Main view
│   │   │   ├── RiskAnalysis.tsx
│   │   │   ├── ScenarioModeller.tsx
│   │   │   └── Recommendations.tsx
│   │   └── components/
│   │       ├── RiskScoreCard.tsx
│   │       ├── ScenarioComparison.tsx
│   │       └── TimelineChart.tsx
│   └── package.json
│
├── .env                             ← API keys here
├── docker-compose.yml               ← Optional infra (unused in prototype)
└── README.md
```

---

## 📅 20-DAY BUILD PLAN

| Days | Milestone | Status | Notes |
|------|-----------|--------|-------|
| 1-2 | Setup APIs + Backend scaffold | 🔴 START | Get NewsAPI, Claude, yfinance working |
| 3-5 | Signal Processor Agent | 🟡 Build | News → extract risk signals |
| 6-8 | Risk Scorer Agent | 🟡 Build | Calculate corridor vulnerability |
| 9-11 | Scenario Modeller Agent | 🟡 Build | Model 30-90 day impacts |
| 12-14 | Recommender Agent | 🟡 Build | Generate procurement actions |
| 15-17 | Frontend Dashboard | 🟡 Build | Risk card, scenarios, recommendations |
| 18-19 | Demo + Polish | 🟡 Build | Make it shine |
| 20 | Buffer | 🟢 DONE | Presentation prep |

---

## 🚀 FIRST 48 HOURS (Checklist)

### Day 1 (July 2)
- [ ] Clone repo structure locally
- [ ] Create `.env` with:
  - `ANTHROPIC_API_KEY=...`
  - `NEWSAPI_KEY=...`
- [ ] Test Claude API connectivity (simple prompt)
- [ ] Test NewsAPI (fetch 5 articles on "Hormuz")
- [ ] Test yfinance (get Brent crude last 30 days)
- [ ] Initialize FastAPI app with one test endpoint
- [ ] Initialize React app (Vite + TypeScript)

### Day 2 (July 3)
- [ ] Build Signal Processor Agent
  - Input: 1 news article about Houthi attack
  - Process: LLM extracts event, corridor, probability
  - Output: JSON with signal
- [ ] Test on 3 real examples:
  - "Houthi attacks Red Sea" → Risk signal ✓
  - "Iran threats US escalation" → Risk signal ✓
  - "Brent crude +8%" → Market signal ✓

---

## 💾 CRITICAL DATA SOURCES

| Data | Source | Free? | Setup |
|------|--------|-------|-------|
| News articles | NewsAPI | ✅ (100/day) | 5 min |
| Brent crude prices | Yahoo Finance | ✅ | 2 min |
| Sanctions | OFAC | ✅ (CSV) | 5 min |
| Historical disruptions | News archives | ✅ | Scrape |
| Geopolitics context | Reuters, CNN | ✅ | Manual |

---

## 🎯 MVP SUCCESS CRITERIA (July 22)

✅ **Must-Have:**
1. Real-time risk score (0-100, updates when news changes)
2. 3-5 scenario forecasts with explicit assumptions
3. 5+ procurement recommendations per scenario
4. Working dashboard (risk + scenarios + recommendations)
5. Demo video (3-5 mins, end-to-end flow)

✅ **Nice-to-Have:**
- Geospatial visualization (Hormuz map + risk zones)
- Historical impact comparison
- Mobile-responsive UI

❌ **Out-of-Scope:**
- Real AIS vessel tracking (use manual tracking)
- Autonomous action execution (recommendations only)
- Detailed economic modeling (simplified models OK)

---

## 🔍 MASTER PROMPT (Share with Collaborators)

**Use this to onboard any LLM or collaborator to the project:**

```markdown
EnergyGuard is an AI energy supply chain resilience system for India.

PROBLEM: 88% crude import dependency, 40-45% via Hormuz (single-point-of-failure).

SOLUTION: Multi-agent LLM system that:
1. Detects geopolitical disruption signals (news + prices + sanctions)
2. Scores corridor risk (0-100 scale)
3. Models 30-90 day impacts (supply, price, reserves, GDP)
4. Recommends procurement strategy (source mix adjustments)

TECH: Python FastAPI backend + React frontend + Claude LLM + SQLite (prototype).

MVP: Risk dashboard + scenario explorer + procurement recommendations.

Deadline: July 22, 2026 (20 days, solo).
```

---

## 🆘 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| NewsAPI returns vague news | Use LLM to interpret sentiment + extract signals |
| Risk score doesn't update | Increase LLM temperature, ensure news is recent (< 24h) |
| Scenario modeling unrealistic | Add physical constraints (refinery max capacity, SPR drain limits) |
| API keys expire/revoked | Set up alerts; keep backup data sources |
| React frontend slow | Use React Query for data fetching, implement caching |
| LLM hallucinating data | Add source citations, validate all numbers against real data |

---

## 📞 QUICK LINKS

| Resource | URL |
|----------|-----|
| Claude API | https://console.anthropic.com/ |
| NewsAPI | https://newsapi.org/ |
| Yahoo Finance | https://finance.yahoo.com/ |
| OFAC Sanctions | https://sanctionslist.ofac.treasury.gov/ |
| IEA Reports | https://www.iea.org/ |
| RBI (India Reserve Bank) | https://www.rbi.org.in/ |
| MITRE ATT&CK | https://attack.mitre.org/ |

---

## 💡 KEY INSIGHTS TO REMEMBER

1. **Simplicity wins:** Don't build perfect models, build working demos
2. **Speed matters:** Early warning (4-8 hours ahead) is valuable
3. **Uncertainty is OK:** Be honest about what you don't know (low confidence)
4. **Domain knowledge is power:** Reference real events (2022 Houthi attacks, 2025 US-Iran standoff)
5. **Judges value realism:** Show assumptions, explain caveats, don't oversell

---

## ✍️ GITHUB DESCRIPTION (348 chars)

```
AI-powered energy supply chain resilience system for India. Real-time disruption 
risk forecasting using geopolitical signals, maritime tracking & commodity intelligence. 
Predicts energy shocks (Hormuz closure, sanctions, shipping attacks) and recommends 
adaptive procurement strategies. Agentic AI + RAG + scenario modelling.
```

---

**Start with Day 1 checklist. You've got this! 🚀**
