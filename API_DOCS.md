# Predictive Intelligence Engine - Real-Time API Documentation

## Overview
This API now supports **real-time data ingestion** from multiple sources for company-wide analytics, forecasting, and decision-making.

---

## New Features

### 1. **File Upload Endpoint** `/upload-dataset`
Upload CSV or Excel files for immediate analysis.

```bash
curl -X POST "http://localhost:8000/upload-dataset" \
  -F "file=@customer_data.csv"
```

**Response:**
```json
{
  "status": "success",
  "message": "Dataset uploaded successfully",
  "data": {
    "filename": "customer_data.csv",
    "rows": 5000,
    "columns": ["date", "revenue", "region", "product"],
    "uploaded_at": "2024-01-15T10:30:45",
    "file_path": "data/uploaded/customer_data.csv"
  }
}
```

---

### 2. **Real-Time Data Ingestion** `/realtime-data`
Stream live data points for continuous analysis.

```bash
curl -X POST "http://localhost:8000/realtime-data" \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_name": "sales_metrics",
    "data": {
      "revenue": 15000,
      "units_sold": 250,
      "region": "North America",
      "date": "2024-01-15"
    },
    "timestamp": "2024-01-15T10:30:45"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Real-time data ingested",
  "dataset": "sales_metrics",
  "timestamp": "2024-01-15T10:30:45"
}
```

---

### 3. **Database Connection** `/database-query`
Connect to your company database and fetch live data.

**Supported Databases:**
- PostgreSQL
- MySQL
- SQLite
- MSSQL

```bash
curl -X POST "http://localhost:8000/database-query" \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "postgresql",
    "host": "db.company.com",
    "port": 5432,
    "username": "analyst",
    "password": "secure_password",
    "database": "production",
    "query": "SELECT * FROM sales WHERE date >= NOW() - INTERVAL 7 day"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Data fetched from database",
  "rows": 2500,
  "columns": ["id", "date", "revenue", "customer_id"],
  "file_path": "data/uploaded/db_query_1705318245.csv"
}
```

---

### 4. **List All Datasets** `/datasets`
View all available datasets (uploaded, cleaned, and from database).

```bash
curl -X GET "http://localhost:8000/datasets"
```

**Response:**
```json
{
  "status": "success",
  "datasets": [
    {
      "name": "customer_data.csv",
      "type": "uploaded",
      "rows": 5000,
      "columns": ["date", "revenue", "region"],
      "path": "data/uploaded/customer_data.csv"
    },
    {
      "name": "Annual_P_L_1_final_cleaned.csv",
      "type": "cleaned",
      "rows": 365,
      "columns": ["date", "revenue", "expenses"],
      "path": "data/cleaned/Annual_P_L_1_final_cleaned.csv"
    }
  ]
}
```

---

### 5. **Real-Time Prediction** `/predict`
Run analysis, forecasting, and decision-making on real-time data.

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_dataset": "data/uploaded/customer_data.csv",
    "forecast_dataset": "data/uploaded/sales_trends.csv",
    "target_column": "revenue",
    "forecast_periods": 30,
    "question": "What will be the revenue trend for next month?",
    "date_columns": ["date", "month"]
  }'
```

**Response:**
```json
{
  "status": "success",
  "analysis": {...},
  "forecast": {...},
  "scenario": {...},
  "rag": {...},
  "decision": {...},
  "timestamp": "2024-01-15T10:30:45"
}
```

---

### 6. **Ask Questions** `/ask`
Ask questions about real-time data using AI.

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the top 3 regions by revenue?"
  }'
```

**Response:**
```json
{
  "status": "success",
  "question": "What are the top 3 regions by revenue?",
  "answer": "Based on the latest data: 1. North America: $2.5M, 2. Europe: $1.8M, 3. APAC: $1.2M",
  "timestamp": "2024-01-15T10:30:45"
}
```

---

### 7. **Interactive Chat** `/chat`
Multi-turn conversation about your data.

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Analyze customer churn patterns",
    "context": "Focus on Q4 2024 data"
  }'
```

**Response:**
```json
{
  "status": "success",
  "question": "Analyze customer churn patterns",
  "answer": "Customer churn increased by 12% in Q4...",
  "context": "Focus on Q4 2024 data",
  "timestamp": "2024-01-15T10:30:45"
}
```

---

## Usage Workflow for Company

### Step 1: Connect Your Data Source
Choose one of three methods:
- **Method A:** Upload CSV/Excel files
- **Method B:** Stream real-time data points
- **Method C:** Connect to company database

### Step 2: List Available Datasets
```bash
GET /datasets
```

### Step 3: Run Analysis
```bash
POST /predict
```

### Step 4: Ask Questions
```bash
POST /ask  or  POST /chat
```

---

## Installation & Running

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Visit: `http://localhost:8000/docs` for interactive API documentation

---

## Data Flow Architecture

```
┌─────────────────────────────────────────┐
│       Data Sources                      │
│  ┌─────────┐  ┌──────────┐  ┌────────┐ │
│  │ CSV/XLS │  │ Database │  │Stream  │ │
│  └────┬────┘  └────┬─────┘  └───┬────┘ │
└───────┼────────────┼────────────┼───────┘
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────▼────────────┐
        │   Real-Time Engine      │
        │  ┌────────────────────┐ │
        │  │ Upload & Ingest    │ │
        │  └────────┬───────────┘ │
        │           │             │
        │  ┌────────▼───────────┐ │
        │  │ AI Agents          │ │
        │  │ • Analysis         │ │
        │  │ • Forecasting      │ │
        │  │ • Scenario Model   │ │
        │  │ • RAG (Q&A)        │ │
        │  │ • Decision Making  │ │
        │  └────────┬───────────┘ │
        └───────────┼──────────────┘
                    │
        ┌───────────▼──────────┐
        │  API Responses       │
        │  • Predictions       │
        │  • Insights          │
        │  • Recommendations   │
        └──────────────────────┘
```

---

## Security Notes

⚠️ **For Production:**
- Never commit database passwords
- Use environment variables for credentials
- Implement API authentication/keys
- Add rate limiting
- Validate file uploads
- Use HTTPS/TLS

```python
# Store credentials securely
from os import getenv
db_password = getenv('DB_PASSWORD')
```

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "status": "error",
  "message": "File not found or unsupported format"
}
```

---

## Support

For issues or questions about real-time data integration:
1. Check dataset structure with `/datasets`
2. Verify file formats (CSV/XLSX)
3. Test database connection parameters
4. Review agent logs for processing errors
