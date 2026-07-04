# EnergyGuard: Energy Supply Chain Resilience System

**AI-powered real-time energy supply disruption forecasting for India**

---

## 🎯 Quick Start (Read These First)

1. **START HERE:** [`00_START_HERE_Executive_Summary.md`](./00_START_HERE_Executive_Summary.md) — Complete overview (5 mins)
2. **DAILY REFERENCE:** [`EnergyGuard_Quick_Reference.md`](./EnergyGuard_Quick_Reference.md) — Cheat sheet (2 mins)
3. **BEFORE CODING:** [`Energy_Guard_Complete_Technical_Setup.md`](./Energy_Guard_Complete_Technical_Setup.md) — Full setup guide (30 mins)

---

## 📚 Complete Documentation

### Problem & Selection
- [`PS_Shortlist_Analysis.md`](./PS_Shortlist_Analysis.md) — Why this problem was chosen
- [`All_PS_Pros_Cons_Matrix.md`](./All_PS_Pros_Cons_Matrix.md) — Detailed pros/cons of all 8 options
- [`Top_3_Quick_Start_Guide.md`](./Top_3_Quick_Start_Guide.md) — Quick-start for top 3 picks

### Technical Implementation
- [`Energy_Guard_Complete_Technical_Setup.md`](./Energy_Guard_Complete_Technical_Setup.md) — Complete setup guide including:
  - API key acquisition (Section 4)
  - Dataset sources (Section 5)
  - Backend architecture (Section 8)
  - Frontend architecture (Section 9)
  - 5 production-ready prompts (Section 7)
  - Master context prompt (Section 11)
  - First 48-hour checklist (Section 12)

### Problem-Solving Methodology
- [`Problem_Solving_Approach.md`](./Problem_Solving_Approach.md) — Deep dive including:
  - Problem decomposition (Section 1)
  - Four-layer solution architecture (Section 2)
  - Comparison with alternatives (Section 3)
  - Implementation strategy (Section 4)
  - Edge cases & mitigation (Section 5)
  - Success metrics (Section 6)
  - 20-day roadmap (Section 7)

---

## 🚀 Project Overview

**Problem:** India imports 88% of crude oil, with 40-45% transiting Hormuz (single-point-of-failure). Current response time to supply shocks: 47 days. Economic cost of delay: Rs 1000s crore.

**Solution:** EnergyGuard — Multi-agent LLM system for real-time disruption forecasting + procurement recommendations.

**Timeline:** 20 days (July 2-22, 2026)

**Tech Stack:**
- Backend: Python (FastAPI) + LangChain (multi-agent) + Claude LLM
- Frontend: React (TypeScript) + Tailwind + Recharts
- Database: SQLite (prototype)
- APIs: NewsAPI, yfinance, OFAC, Claude, OpenWeatherMap

---

## 📊 Architecture at a Glance

```
NEWS FEEDS
  ↓
[SIGNAL PROCESSOR] → Extract risk signals (news → {event, corridor, probability})
  ↓
[RISK SCORER] → Calculate vulnerability (0-100 scale)
  ↓
[SCENARIO MODELLER] → Forecast 30-90 day impacts
  ↓
[RECOMMENDER] → Generate procurement strategy
  ↓
DASHBOARD → Risk card | Scenarios | Recommendations | Timeline
```

---

## 🎯 Key Features

### 1. Signal Detection
- Monitors geopolitical news in real-time
- Extracts disruption probabilities automatically
- Tracks Hormuz shipping patterns
- Monitors sanctions updates

### 2. Risk Scoring
- Calculates corridor vulnerability (0-100)
- Combines probability × impact
- Provides confidence levels
- Shows historical baseline comparison

### 3. Scenario Modeling
- Projects 30-90 day impacts
- Shows cascade effects:
  - Supply loss → SPR burn rate
  - Price spike → refinery stress
  - Demand reduction → economic impact
- Explicit assumptions documented

### 4. Procurement Recommendations
- Specific, prioritized actions:
  - "Increase Russia supply 300K bbl/day (delivery in 12 days)"
  - "Activate spot market 500K bbl/day (3 days)"
  - "Manage SPR drawdown at max capacity"
- Timeline + cost + risk estimates for each

### 5. Executive Dashboard
- Risk score at a glance
- Scenario comparison (side-by-side)
- Timeline forecasts (Day 1, 5, 10, 30)
- Evidence layer (click through to sources)

---

## 🔑 API Keys Needed (30-min setup)

```bash
ANTHROPIC_API_KEY      # Claude LLM ($50-100 for hackathon)
NEWSAPI_KEY            # Geopolitical signals (free tier: 100/day)
DATABASE_URL=sqlite:///./energem.db  # Local prototype DB
# yfinance             # Commodity prices (no key, pip install yfinance)
# OFAC Registry        # Sanctions (no key, download CSV)
```

**Total setup time:** 30 minutes  
**Total cost:** ~$50-100  

---

## 📅 20-Day Sprint Plan

| Phase | Days | Milestone | Deliverable |
|-------|------|-----------|-------------|
| Setup | 1-2 | APIs + backend scaffold | Working FastAPI + LLM connectivity |
| Agent 1 | 3-5 | Signal Processor | News → risk signals JSON |
| Agent 2 | 6-8 | Risk Scorer | Corridor risk 0-100 scores |
| Agent 3 | 9-11 | Scenario Modeller | 30-day impact forecasts |
| Agent 4 | 12-14 | Recommender | Procurement strategies |
| UI | 15-17 | Dashboard | React UI with 4+ views |
| Demo | 18-19 | Video + Polish | End-to-end demonstration |
| Buffer | 20 | Final checks | Presentation ready |

---

## ✅ MVP Success Criteria

**Must-Have by July 22:**
- [ ] Real-time risk score (updates as news changes)
- [ ] 3-5 scenario forecasts with explicit assumptions
- [ ] 5+ procurement recommendations per scenario
- [ ] Working web dashboard
- [ ] Demo video (3-5 mins, end-to-end)
- [ ] Architecture diagram
- [ ] Working prototype on GitHub

**Nice-to-Have:**
- [ ] Geospatial visualization (risk heatmap)
- [ ] Mobile-responsive UI
- [ ] Historical impact comparison

**Out-of-Scope:**
- ❌ Real AIS tracking (use manual + news)
- ❌ Autonomous execution (recommendations only)
- ❌ Full GDP modeling (simplified)

---

## 📖 How to Use These Documents

### For Implementation
1. Start with [`EnergyGuard_Quick_Reference.md`](./EnergyGuard_Quick_Reference.md) — keep this on your desk
2. Follow [`Energy_Guard_Complete_Technical_Setup.md`](./Energy_Guard_Complete_Technical_Setup.md) for full setup
3. Reference specific prompts in Section 7 of Technical Setup
4. Check 20-day timeline in Section 7 of Problem-Solving Approach

### For Presentations
1. Use [`Problem_Solving_Approach.md`](./Problem_Solving_Approach.md) for problem framing
2. Reference [`PS_Shortlist_Analysis.md`](./PS_Shortlist_Analysis.md) if judges ask "why this PS?"
3. Show architecture from Problem-Solving Approach Section 2

### When Stuck
1. Check troubleshooting section in Quick Reference
2. Review Problem-Solving Approach Section 5 (edge cases)
3. Look at "Common Issues & Solutions" in Technical Setup Section 11

### For Demo & Pitch
1. Keep 30-second pitch from Executive Summary ready
2. Use architecture diagrams from Problem-Solving Approach
3. Have success metrics (Section 6 of Problem-Solving) handy

---

## 🎯 Key Concepts

**Risk Score (0-100):**
- 0-20: Low (routine)
- 20-40: Moderate (watchful)
- 40-60: High (contingency planning)
- 60-80: Very High (activate alternatives)
- 80-100: Critical (emergency measures)

**Corridors of Interest:**
1. **Hormuz Strait** (40-45% of Indian imports) — Chokepoint risk
2. **Red Sea** (alternative route) — Houthi attacks
3. **Suez Canal** (Egypt transit) — Political instability
4. **Malacca Strait** (alternate shipping) — Piracy + geopolitics
5. **Land/Rail Routes** (Russia, Central Asia) — Sanctions risk

**Key Metrics:**
- Supply gap (barrels/day)
- SPR burn rate (days remaining)
- Price spike (Brent multiple)
- Refinery impact (% run reduction)
- GDP impact (annualized growth reduction)

---

## 💡 Quick Commands

```bash
# Setup Python environment
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn langchain anthropic httpx pydantic

# Setup React frontend
npm create vite@latest frontend -- --template react-ts
cd frontend && npm install

# Test APIs
python -c "import newsapi; print('NewsAPI working')"
python -c "import yfinance; print('yfinance working')"
python -c "from anthropic import Anthropic; print('Claude working')"

# Start FastAPI dev server
cd backend
python -m uvicorn backend.main:app --reload --port 8000

# SQLite prototype maintenance
python scripts/sqlite_tools.py status
python scripts/sqlite_tools.py backup
python scripts/sqlite_tools.py reset

# Start React dev server
npm run dev
```

---

## 📞 Resource Links

| Resource | URL |
|----------|-----|
| Claude API | https://console.anthropic.com/ |
| NewsAPI | https://newsapi.org/ |
| Yahoo Finance | https://finance.yahoo.com/ |
| OFAC Sanctions | https://sanctionslist.ofac.treasury.gov/ |
| IEA Reports | https://www.iea.org/ |
| RBI (India) | https://www.rbi.org.in/ |
| MITRE ATT&CK | https://attack.mitre.org/ |

---

## 🏆 Why This Project Wins

✅ **Innovation:** First multi-agent LLM system for energy supply chain resilience  
✅ **Impact:** Prevents Rs 1000s crore supply shock damage  
✅ **Feasibility:** All data public, all tech mature, solo-buildable in 20 days  
✅ **Scalability:** Works for Japan, South Korea, semiconductors, rare earths  
✅ **Urgency:** India's 88% import dependency is real and pressing  

---

## 📝 File Organization

```
/outputs/
├── 00_START_HERE_Executive_Summary.md          ← Read this first!
├── EnergyGuard_Quick_Reference.md              ← Daily cheat sheet
├── Energy_Guard_Complete_Technical_Setup.md    ← Full technical guide
├── Problem_Solving_Approach.md                 ← Deep methodology
├── PS_Shortlist_Analysis.md                    ← PS selection justification
├── All_PS_Pros_Cons_Matrix.md                  ← All options evaluated
├── Top_3_Quick_Start_Guide.md                  ← Alternative starts
└── README.md                                    ← This file
```

---

## 🚀 Next Steps (Right Now)

1. **Read** [`00_START_HERE_Executive_Summary.md`](./00_START_HERE_Executive_Summary.md) (5 mins)
2. **Get** API keys (30 mins) — follow section 4 of Technical Setup
3. **Initialize** GitHub repo + scaffold (30 mins)
4. **Build** Signal Processor Agent (by July 3) — your north star
5. **Iterate** through remaining agents (Days 6-14)
6. **Polish** UI + demo (Days 15-20)

---

## 💬 30-Second Pitch

```
"EnergyGuard is an AI system that detects energy supply disruptions 
before they cause economic damage. It monitors geopolitical events, 
commodity markets, and shipping data in real time, models the impact 
over 30-90 days, and recommends specific procurement strategies to 
keep India's supply chain resilient."
```

---

**Status:** ✅ READY TO BUILD  
**Timeline:** 20 days (July 2-22, 2026)  
**Confidence:** 95% (very doable)  

**Let's go! 🚀**

