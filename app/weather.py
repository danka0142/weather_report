from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import httpx
import uvicorn

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
    url = "https://api.openweathermap.org/data/4.0/onecall/current"
    params = {
        "lat": 55.7558,
        "lon": 37.6176,
        "units": "metric",
        "lang": "ru",
        "appid": API_KEY,
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        data_list = data.get("data", [])
        if not data_list:
            raise HTTPException(status_code=502, detail="OpenWeatherMap returned empty data array")

        current = data_list[0]

        weather_list = current.get("weather", [])
        if not weather_list:
            raise HTTPException(status_code=502, detail="OpenWeatherMap returned empty weather array")

        return {
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "timezone": data.get("timezone"),
            "temperature": current.get("temp"),
            "feels_like": current.get("feels_like"),
            "humidity": current.get("humidity"),
            "pressure": current.get("pressure"),
            "wind_speed": current.get("wind_speed"),
            "wind_deg": current.get("wind_deg"),
            "clouds": current.get("clouds"),
            "visibility": current.get("visibility"),
            "sunrise": current.get("sunrise"),
            "sunset": current.get("sunset"),
            "description": weather_list[0].get("description"),
            "icon": weather_list[0].get("icon"),
        }

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"OpenWeatherMap error: {e.response.text}")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Connection error")
    except ValueError:
        raise HTTPException(status_code=502, detail="Invalid JSON from OpenWeatherMap")


if __name__ == "__main__":
    uvicorn.run("weather:app", reload=True)
