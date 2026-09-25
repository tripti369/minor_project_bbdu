# Quick Command Reference

## Current Status
- ✅ Server running on port 8000
- ✅ All dependencies installed
- ⏳ Waiting for your Gemini API key

## To Enable Gemini AI (Survival Mode - 2 Steps)

### Step 1: Add API Key
```powershell
# Open the .env file and edit it:
notepad .env

# Find this line:
GEMINI_API_KEY=your_gemini_api_key_here

# Replace with your actual key from:
# https://aistudio.google.com/app/apikey
```

### Step 2: Restart Server
```powershell
# In the terminal running uvicorn:
# Press CTRL+C to stop

# Then run:
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Test Endpoints

### Health Check
```bash
curl http://localhost:8000/
```
**Shows**: AI engine status ("Gemini AI" or "Local RAG")

### Chat with AI (Gemini)
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is time series forecasting?", "context": "I have sales data"}'
```

### Quick Q&A (Gemini)
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I improve forecast accuracy?"}'
```

### Upload Data
```bash
curl -X POST "http://localhost:8000/upload-dataset" \
  -F "file=@path/to/your/data.csv"
```

### List Available Datasets
```bash
curl http://localhost:8000/datasets
```

### Make Predictions
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_dataset": "your_file.csv",
    "forecast_dataset": "your_file.csv",
    "target_column": "sales",
    "forecast_periods": 12,
    "question": "What will sales be next quarter?"
  }'
```

## Run Test Suite

### Automated Tests
```powershell
python test_gemini_integration.py
```

### Original System Tests
```powershell
python test_realtime_system.py
```

## API Documentation (Interactive)

Open browser: `http://localhost:8000/docs`
- Try out endpoints live
- See request/response examples
- Auto-generated from code

## Stop Server

```powershell
# In the terminal running uvicorn:
Ctrl+C
```

## Restart Server

```powershell
cd C:\Users\tript\OneDrive\Desktop\predictive-intelligence-engine
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## File Locations

```
C:\Users\tript\OneDrive\Desktop\predictive-intelligence-engine\
├── .env                          # ← Edit this, add API key
├── app.py                         # Main API
├── requirements.txt               # Dependencies
├── GEMINI_SETUP.md               # Full setup guide
├── INTEGRATION_STATUS.md         # This status report
├── test_gemini_integration.py    # Gemini tests
├── test_realtime_system.py       # System tests
├── data/
│   ├── cleaned/                  # Sample data
│   ├── uploaded/                 # Your uploads
│   └── realtime/                 # Live streams
└── agents/                        # AI agents
    ├── analysis_agent.py
    ├── forecasting_agent.py
    ├── scenario_agent.py
    ├── rag_agent.py
    └── decision_agent.py
```

## Key Milestones

| ✅ Done | Task |
|--------|------|
| ✅ | Install dependencies |
| ✅ | Start FastAPI server |
| ✅ | Add Gemini SDK |
| ✅ | Update app.py with AI |
| ✅ | Create .env config |
| ✅ | Write documentation |
| ⏳ | **← Add your API key (YOU ARE HERE)** |
| ⏳ | Restart server |
| ⏳ | Test /chat endpoint |
| ⏳ | Test /ask endpoint |
| ⏳ | Upload your data |
| ⏳ | Run predictions |

## Gemini Free Tier Limits

- 60 requests per minute
- 1500 requests per day
- Generous for testing & development

Check usage: https://console.cloud.google.com/

## Common Issues & Fixes

### Issue: "ai_engine" still "Local RAG"
```powershell
# Check if .env is being read:
echo $env:GEMINI_API_KEY

# If empty, restart server
# If showing key, then working!
```

### Issue: Chat takes 10+ seconds
- Normal for Gemini API (2-5s is typical)
- Check internet connection
- Check Google Cloud quota

### Issue: "Not authenticated with API key"
- Verify key in .env
- Get new key from: https://aistudio.google.com/app/apikey
- Restart server
- Test: `python test_gemini_integration.py`

## What's AI-Enhanced

✨ These endpoints use Gemini when available:
- `/chat` - Interactive conversation
- `/ask` - Quick questions

🔹 These endpoints work regardless:
- `/predict` - Uses local agents (now with better context)
- `/upload-dataset` - File handling
- `/database-query` - Database integration

## Success Indicators

After adding your API key, you'll see:

```json
{
  "status": "success",
  "question": "Your question?",
  "answer": "Gemini AI response here...",
  "ai_engine": "Gemini AI",
  "timestamp": "2024-01-01T12:00:00"
}
```

Key indicator: `"ai_engine": "Gemini AI"` ✅

---

## Next Steps

```powershell
1. Get API key from: https://aistudio.google.com/app/apikey
2. Edit .env file: notepad .env
3. Add: GEMINI_API_KEY=your_actual_key
4. Restart server: Ctrl+C, then python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
5. Test: python test_gemini_integration.py
```

## System Status

```
FastAPI Server: ✅ RUNNING on http://0.0.0.0:8000
Python Version: 3.14+
Database Support: ✅ PostgreSQL, MySQL, SQLite, MSSQL
Data Formats: ✅ CSV, Excel, JSON, SQL
AI Engine: ⏳ AWAITING API KEY
Status: 🟡 Ready - Just need your Gemini key!
```

---

**Ready to go! Just add your API key and restart.** 🚀
