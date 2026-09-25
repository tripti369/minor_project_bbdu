# Gemini API Integration Guide

## Quick Start (Survival Mode)

Your Predictive Intelligence Engine now includes **Gemini AI** for enhanced Q&A capabilities!

### Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### Step 2: Set Up Environment

1. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 3: Restart Server

The server automatically loads your `.env` file on startup. If it's already running, you can:
- Press `CTRL+C` to stop uvicorn
- Run: `python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000`

### Step 4: Test Gemini Integration

**Test /chat endpoint:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the best practices for forecasting time series data?",
    "context": "I have 24 months of sales data"
  }'
```

**Response with Gemini enabled:**
```json
{
  "status": "success",
  "question": "What are the best practices for forecasting time series data?",
  "answer": "[Gemini's AI-powered response]",
  "ai_engine": "Gemini AI",
  "timestamp": "2024-01-01T12:00:00"
}
```

**Response without Gemini (fallback):**
```json
{
  "ai_engine": "Local RAG",
  ...
}
```

## Features Enabled by Gemini

### 1. `/ask` - Quick Answers
- Ask any data-related question
- Gemini provides instant AI-powered responses

### 2. `/chat` - Interactive Conversation
- Multi-turn conversations with context
- Contextual understanding of your data

### 3. `/predict` - Enhanced Insights
- Combines predictions with AI reasoning
- More human-readable explanations

## API Status Check

Visit `http://localhost:8000/docs` and check the home endpoint response:
```json
{
  "message": "Predictive Intelligence Engine Running",
  "version": "2.1",
  "ai_engine": "Gemini AI",  // Shows your AI engine status
  "status": "ready"
}
```

## Troubleshooting

**Q: Getting "ModuleNotFoundError: No module named 'google'"?**
- Run: `pip install google-generativeai`

**Q: Gemini API returns errors?**
- Check your API key is correct: `echo $env:GEMINI_API_KEY` (PowerShell)
- Verify key is valid at [Google AI Studio](https://aistudio.google.com/app/apikey)
- Check API quota and usage limits

**Q: Still using "Local RAG" instead of Gemini?**
1. Verify `.env` file exists in project root
2. Check `GEMINI_API_KEY` is set correctly
3. Restart the server
4. Check server logs for errors

**Q: Rate limit exceeded?**
- Gemini API has usage limits
- Implement request caching or queue system (optional upgrade)

## Security Best Practices

⚠️ **IMPORTANT:**
- Never commit `.env` to version control
- Don't share your API key
- Use `.gitignore` to exclude `.env`:

```bash
echo ".env" >> .gitignore
```

## Endpoints Using Gemini

| Endpoint | Gemini | Fallback |
|----------|--------|----------|
| `/chat` | ✅ AI Conversation | Local RAG |
| `/ask` | ✅ Quick Answers | Local RAG |
| `/predict` | ❌ (Uses agents) | Agents |
| `/upload-dataset` | ❌ | File handling |
| `/database-query` | ❌ | SQL queries |

## Next Steps

1. ✅ Set up `.env` with API key
2. ✅ Test `/chat` and `/ask` endpoints
3. Upload real data: `/upload-dataset`
4. Run predictions: `/predict`
5. Ask questions: `/chat` or `/ask`

## Performance Tips

- Gemini responses typically take 2-5 seconds
- Cache frequently asked questions
- Use `/ask` for quick, direct questions
- Use `/chat` for nuanced, conversational queries

## Cost Monitoring

Monitor your Gemini API usage:
- Visit [Google Cloud Console](https://console.cloud.google.com/)
- Check your billing and quota usage
- Set up budget alerts if needed

---

**System Status**: ✅ Ready for Production
**AI Engine**: Gemini AI 
**Server**: Running on `http://0.0.0.0:8000`
