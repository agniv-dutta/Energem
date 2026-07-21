# Energem

**AI-powered real-time energy supply chain resilience system for India**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-FF6B00?style=flat&logo=groq&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

---

India imports 88% of its crude oil, with 40-45% transiting the Strait of Hormuz - a single point of failure. Current response time to supply shocks: 47 days. Energem detects disruptions 4-8 hours before market reaction, forecasts 30-90 day impact cascades, and recommends specific procurement actions - compressing response from 47 days to 47 minutes.

---

## Architecture

```
News Feeds / Maritime Data / Sanctions Registries
              │
              ▼
    ┌─────────────────────┐
    │   SIGNAL PROCESSOR   │  Extract risk signals from raw data
    └─────────┬───────────┘
              ▼
    ┌─────────────────────┐
    │     RISK SCORER      │  Score corridor vulnerability (0-100)
    └─────────┬───────────┘
              ▼
    ┌─────────────────────┐
    │  SCENARIO MODELLER   │  Forecast 30-90 day impact cascades
    └─────────┬───────────┘
              ▼
    ┌─────────────────────┐
    │    RECOMMENDER       │  Generate procurement strategies
    └─────────┬───────────┘
              ▼
         Dashboard
```

## Features

- **Signal Detection** — Real-time geopolitical signal extraction via NewsAPI + LLM analysis
- **Risk Scoring** — Corridor vulnerability scoring (0-100) across 5 chokepoints: Hormuz, Red Sea, Malacca, Suez, Land/Rail
- **Scenario Simulation** — Model disruption severity and duration, project SPR exhaustion timelines, price spikes, and supply deficits
- **Procurement Intelligence** — Specific, prioritized actions with volume, ETA, cost premium, and geopolitical risk per recommendation
- **Corridor Map** — P&ID-style schematic with color-coded risk visualization and live polling

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, LangChain, Groq LLM |
| Frontend | React 19, TypeScript, Vite, Zustand, Framer Motion |
| Database | SQLite + SQLAlchemy |
| APIs | NewsAPI, yfinance, Groq |

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- API keys: `GROQ_API_KEY`, `NEWSAPI_KEY`

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

```bash
# backend/.env
GROQ_API_KEY=gsk_...
NEWSAPI_KEY=...

# frontend/.env
VITE_API_BASE_URL=http://localhost:8000
```

## Project Structure

```
Energem/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Environment configuration
│   ├── agents/              # LangChain multi-agent system
│   ├── api/                 # Route handlers
│   ├── services/            # Business logic
│   ├── db/                  # SQLAlchemy models
│   └── data/                # Static datasets
├── frontend/
│   └── src/
│       ├── pages/           # Dashboard, CorridorMap, Simulator, Procurement, Intelligence
│       ├── components/      # Shared UI components
│       ├── services/        # API client
│       └── store/           # Zustand state management
└── docker-compose.yml
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/landing` | GET | Landing page risk summary |
| `/api/corridors/status` | GET | Live corridor risk scores |
| `/api/signals/latest` | GET | Latest intelligence signals |
| `/api/scenarios/simulate` | POST | Run disruption simulation |
| `/api/procurement/recommendations` | GET | Procurement recommendations |
| `/api/procurement/authorize` | POST | Authorize procurement actions |

## License

MIT
