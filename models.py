from pydantic import BaseModel
import requests
from fastapi import HTTPException
from tools import WEATHER_API_KEY

#api_key = WEATHER_API_KEY

class currentweather(BaseModel):
    name: str
    temperature: str
    wind : str

class WeatherList(BaseModel):
    city : list[currentweather]    

class WeatherAPIError(BaseModel):
   "this is WeatherAPIError"

def weather(city: list[str]):
    if not WEATHER_API_KEY:
        raise HTTPException(
            status_code=500,
            detail= "openweather API Key is missing"
        )
    
    url= "https://api.openweathermap.org/data/2.5/weather"
    params={
        "q": city,
        "appid": WEATHER_API_KEY,
        "units":"metric"
    }  

    response = requests.get(url,params=params)
    #print(response)
    
    if response.status_code != 200: 
        try:
            message = response.json().get("message","unable to fetch weather")
        except ValueError:
            message = "unable to fetch weather"    
        return {"error": message}
    data = response.json()
    #print(data)
    return data  

class chatRequest(BaseModel):
    user_input: str

class chatResponse(BaseModel):
    reply: str    