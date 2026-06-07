from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import httpx
import uvicorn
from fetch_as_json import fetch_latest_weather_json
from dotenv import load_dotenv
from os import getenv
load_dotenv()
API_KEY =getenv("API_KEY")


app = FastAPI()

@app.get("/")
async def index():
    return FileResponse("index.html")


@app.get("/weather")
async def weather():

    data = await fetch_latest_weather_json()

    if not data:
        raise HTTPException(status_code=404, detail="Данные о погоде не найдены в базе")

    # 2. Формируем плоский ответ для фронтенда из структуры БД
    return {
        "lat": data["coordinates"]["lat"],
        "lon": data["coordinates"]["lon"],
        "timezone": data["timezone"],
        "temperature": data["weather"]["temperature"],
        "feels_like": data["weather"]["feels_like"],
        "humidity": data["weather"]["humidity"],
        "pressure": data["weather"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "wind_deg": data["wind"]["deg"],
        "clouds": data["clouds"],
        "visibility": data["visibility"],
        "sunrise": data["astronomy"]["sunrise"],
        "sunset": data["astronomy"]["sunset"],
        "description": data["info"]["description"],
        "icon": data["info"]["icon"],
    }




if __name__ == "__main__":
    uvicorn.run("weather:app", reload=True)
