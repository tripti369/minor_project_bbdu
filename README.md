# Deployed link- https://radhe-radhe-sarthi-ai.onrender.com/

# Team members with their roles 
# Backend — Predictive Intelligence Engine API

FastAPI + SQLite backend. Real CSV data, real database, no mock endpoints.

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

or directly with uvicorn:

```bash
uvicorn app.main:app --reload --port 8000
```

Server: `http://127.0.0.1:8000`
Interactive API docs: `http://127.0.0.1:8000/docs`

## Configuration

Copy `.env.example` to `.env` and adjust if needed:

```bash
cp .env.example .env
```

| Variable       | Default                     | Meaning |
|----------------|------------------------------|---------|
| `PORT`         | `8000`                       | Port the server listens on |
| `DATABASE_URL` | `sqlite:///./data/app.db`    | Where the SQLite file lives |
| `CORS_ORIGINS` | `*`                          | Comma-separated allowed frontend origins |

## Folder guide

```
backend/
├── app/
│   ├── main.py            # FastAPI app, CORS, route registration
│   ├── database.py        # SQLAlchemy engine/session + init_db()
│   ├── models.py          # DB tables: PredictionRun, ScenarioRun, UploadedDataset
│   ├── schemas.py         # Pydantic response models
│   ├── utils.py           # Shared CSV-loading helper
│   ├── agents/
│   │   ├── analysis_agent.py      # stats / correlation / outliers
│   │   ├── forecasting_agent.py   # Holt-Winters + moving-average fallback
│   │   ├── scenario_agent.py      # Monte Carlo simulation
│   │   ├── rag_agent.py           # TF-IDF retrieval over data/knowledge
│   │   └── decision_agent.py      # combines everything into a recommendation
│   └── routes/
│       ├── predict.py     # GET /api/predict
│       ├── analysis.py    # GET /api/analysis
│       ├── scenario.py    # GET /api/scenario
│       ├── upload.py      # POST /api/upload
│       ├── knowledge.py   # GET /api/knowledge
│       ├── history.py     # GET /api/history
│       └── datasets.py    # GET /api/datasets
└── data/
    ├── cleaned/    # shipped datasets (do not edit — these are the demo data)
    ├── uploaded/   # files uploaded via POST /api/upload land here
    ├── knowledge/  # markdown notes the RAG agent indexes
    └── app.db      # created automatically on first run
```

## Adding a new dataset

Drop a CSV into `data/cleaned/` (or upload it through `/api/upload`, which
saves it to `data/uploaded/`), then reference its filename in a request,
e.g. `GET /api/analysis?dataset=your_file.csv`.

## Adding a new API route

1. Create `app/routes/your_route.py` with an `APIRouter()`.
2. Register it in `app/main.py`:
   ```python
   from app.routes import your_route
   app.include_router(your_route.router, prefix="/api", tags=["Your Feature"])
   ```

## Resetting the database

The database is a single file — just delete it and restart the server,
it will be recreated empty:

```bash
rm data/app.db
python run.py
```
