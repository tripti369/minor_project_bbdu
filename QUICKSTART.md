# 🚀 Quick Start Guide - Real-Time Predictive Intelligence Engine

## Installation (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: `http://localhost:8000`

---

## Three Ways to Use With Real-Time Data

### Option A: Upload CSV File (Fastest)

**Step 1:** Upload your company data
```bash
curl -F "file=@your_sales_data.csv" http://localhost:8000/upload-dataset
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "filename": "your_sales_data.csv",
    "rows": 5000,
    "columns": ["date", "revenue", "region"]
  }
}
```

**Step 2:** Run prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_dataset": "your_sales_data.csv",
    "forecast_dataset": "your_sales_data.csv",
    "target_column": "revenue",
    "forecast_periods": 12,
    "question": "What will revenue be next quarter?"
  }'
```

---

### Option B: Connect to Database (Production)

```bash
curl -X POST http://localhost:8000/database-query \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "postgresql",
    "host": "your-db.company.com",
    "port": 5432,
    "username": "user",
    "password": "password",
    "database": "sales_db",
    "query": "SELECT date, revenue FROM sales WHERE date >= CURRENT_DATE - 90"
  }'
```

Supported databases:
- ✅ PostgreSQL
- ✅ MySQL
- ✅ MSSQL
- ✅ SQLite

---

### Option C: Stream Real-Time Data

```bash
curl -X POST http://localhost:8000/realtime-data \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_name": "hourly_metrics",
    "data": {
      "timestamp": "2024-01-15T14:00:00",
      "revenue": 25000,
      "units": 320,
      "region": "North America"
    }
  }'
```

---

## Ask Questions About Your Data

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the revenue trend by region?"
  }'
```

---

## View Available Datasets

```bash
curl http://localhost:8000/datasets
```

Lists all:
- Uploaded files
- Pre-cleaned datasets
- Database exports
- Real-time data streams

---

## Full Pipeline: From Data to Decision

```
1. UPLOAD DATA
   └─ /upload-dataset
   
2. LIST DATASETS  
   └─ /datasets
   
3. RUN PREDICTION
   ├─ Analysis
   ├─ Forecasting
   ├─ Scenarios
   ├─ RAG (Knowledge Base)
   └─ Decision
   
4. ASK QUESTIONS
   └─ /chat or /ask
   
5. GET INSIGHTS
   └─ Decision recommendations
```

---

## Example: End-to-End Flow

```python
import requests

# 1. Upload your CSV
with open("Q1_sales.csv", "rb") as f:
    r = requests.post("http://localhost:8000/upload-dataset", 
                      files={"file": f})
    filename = r.json()["data"]["filename"]
    print(f"✓ Uploaded: {filename}")

# 2. Run prediction on uploaded data
response = requests.post("http://localhost:8000/predict", json={
    "analysis_dataset": filename,
    "forecast_dataset": filename,
    "target_column": "revenue",
    "forecast_periods": 12,
    "question": "Forecast next quarter?"
})

result = response.json()
print("✓ Analysis:", result["analysis"]["basic_statistics"]["rows"], "rows")
print("✓ Forecast:", result["forecast"]["model"])
print("✓ Decision:", result["decision"]["risk"], "risk")

# 3. Ask follow-up questions
response = requests.post("http://localhost:8000/chat", json={
    "question": "What are the top risks?"
})
print("✓ Answer:", response.json()["answer"])
```

---

## Key Features

✅ **Real-Time Data Integration**
- Upload CSV/Excel files instantly
- Connect to company databases
- Stream live data points

✅ **Advanced Analytics**
- Statistical analysis
- Trend detection
- Outlier detection
- Correlation analysis

✅ **AI-Powered Forecasting**
- Time series prediction
- Multiple scenarios (Best/Base/Worst)
- Accuracy metrics

✅ **Intelligent Q&A**
- Ask questions in natural language
- AI answers based on your data
- Context-aware responses

✅ **Business Decisions**
- Risk assessment
- Recommendations
- Executive summaries

---

## Common Commands

| Task | Endpoint | Method |
|------|----------|--------|
| Upload file | `/upload-dataset` | POST |
| Query database | `/database-query` | POST |
| Stream real-time | `/realtime-data` | POST |
| List datasets | `/datasets` | GET |
| Run prediction | `/predict` | POST |
| Ask question | `/chat` | POST |
| Quick answer | `/ask` | POST |

---

## Troubleshooting

**"Dataset not found"**
- Check file exists in `data/uploaded/`
- Use `/datasets` to list available files
- Verify filename exactly

**"Database connection failed"**
- Verify host/port/credentials
- Check firewall allows connection
- Test with command line first

**"Slow performance"**
- Use smaller datasets initially
- Check available RAM
- Reduce forecast_periods

**"Column not found"**
- Column names are case-sensitive
- Check date column exists
- Use `/datasets` to verify columns

---

## What Changed for Real-Time Support

✅ **Agents Now Support Dynamic File Paths**
- `analysis_agent.py` - Updated `load_dataset()`
- `forecasting_agent.py` - Updated `load_dataset()`
- Searches: uploaded → realtime → cleaned directories

✅ **New API Endpoints**
- `/upload-dataset` - Upload files
- `/realtime-data` - Stream data points
- `/database-query` - Connect to databases
- `/datasets` - List all data sources

✅ **Better Error Handling**
- Searches multiple locations
- Clear error messages
- Shows searched paths

✅ **Production Ready**
- Database integration (PostgreSQL, MySQL, MSSQL, SQLite)
- Cross-platform file paths
- Security best practices

---

## API Documentation

Interactive API docs available at:
- **Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Next Steps

1. ✅ Install requirements: `pip install -r requirements.txt`
2. ✅ Start server: `uvicorn app:app --reload`
3. ✅ Upload a CSV file
4. ✅ Run prediction
5. ✅ Ask questions
6. 📖 Read `REALTIME_SETUP.md` for detailed setup
7. 🔧 See `REALTIME_EXAMPLES.py` for code examples

---

**Need Help?**
- Check `API_DOCS.md` for detailed API reference
- See `REALTIME_SETUP.md` for configuration guide
- Run `REALTIME_EXAMPLES.py` for working examples
