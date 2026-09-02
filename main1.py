import ollama
import json
from models import weather, WeatherList, askBotRequest, askBotResponse,WeatherAPIError
from prompts import SYSTEM_PROMPT
from tools import TOOLS
from fastapi import FastAPI, HTTPException


MODEL = "llama3.2"
app = FastAPI()


OPTIONS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "num_predict": 300,
    "num_ctx": 4096,
}

@app.post('/askbot', response_model=askBotResponse)
def ChatBot(payload: askBotRequest):
    return ""