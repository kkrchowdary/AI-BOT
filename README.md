# AI-BOT

A small FastAPI-based chatbot that uses an LLM (via ollama) and simple tools.

## Quickstart

1. Copy `.env.example` to `.env` and set any required environment variables.
2. Install dependencies (example):

```bash
pip install -r requirements.txt
```

3. Run locally with uvicorn:

```bash
uvicorn main:app --reload
```

4. POST JSON to `/chat`:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "What's the weather in London?"}'
```

## Notes

- The `models.weather` function currently returns mocked weather data. Replace
  with a real API integration when ready.
- The `TOOLS` list is intentionally empty; add tool descriptors when you add
  tool implementations.
