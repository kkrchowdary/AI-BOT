# AI-BOT

FastAPI chatbot via Ollama + a weather tool.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Run

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Docs: http://127.0.0.1:8000/docs

## Debug

Run and Debug → **Debug FastAPI** → F5. Set breakpoint. Hit `/chat`.

No `--reload` while debugging (child process skips breakpoints).

## Notes

- Needs Ollama + model `llama3.2` (or change `MODEL` in `main.py`).
- `models.weather` is mocked until you set a real weather API in `.env`.
