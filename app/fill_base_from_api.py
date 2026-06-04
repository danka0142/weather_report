import database
import model
#from sqlalchemy.orm import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
import httpx
import asyncio

from dotenv import load_dotenv
from os import getenv
load_dotenv()
API_KEY =getenv("API_KEY")

import httpx
from datetime import datetime

async def fetch_and_save_weather():
    url = "https://api.openweathermap.org/data/4.0/onecall/current"
    lat, lon = 55.7558, 37.6176
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "lang": "ru",
        "appid": API_KEY,
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        
        # 1. Валидация структуры ответа (из вашего эндпоинта FastAPI)
        data_list = data.get("data", [])
        if not data_list:
            print("Ошибка: OpenWeatherMap вернул пустой массив 'data'")
            return

        current = data_list[0]
        weather_list = current.get("weather", [])
        if not weather_list:
            print("Ошибка: OpenWeatherMap вернул пустой массив 'weather'")
            return

        # 2. Создание записи для базы данных на основе новой модели WeatherData
        weather_record = model.WeatherData(
            lat=data.get("lat"),
            lon=data.get("lon"),
            timezone=data.get("timezone"),
            temperature=current.get("temp"),
            feels_like=current.get("feels_like"),
            humidity=current.get("humidity"),
            pressure=current.get("pressure"),
            wind_speed=current.get("wind_speed"),
            wind_deg=current.get("wind_deg"),
            clouds=current.get("clouds"),
            visibility=current.get("visibility"),
            
            # Конвертируем Unix timestamp (int) в datetime объект timezone-naive
            sunrise=datetime.fromtimestamp(current.get("sunrise")),
            sunset=datetime.fromtimestamp(current.get("sunset")),
            
            description=weather_list[0].get("description"),
            icon=weather_list[0].get("icon")
        )
        

        Session = async_sessionmaker(bind=database.async_engine, class_=AsyncSession, expire_on_commit=False)

        async with Session() as session:
            async with session.begin():  # Автоматически сделает commit() при успехе или rollback() при ошибке
                session.add(weather_record)
                
        print(f"Данные погоды для {data.get('timezone')} успешно сохранены в БД.")
        
    except httpx.HTTPStatusError as e:
        print(f"Ошибка API OpenWeatherMap: {e.response.text}")
    except httpx.RequestError as e:
        print(f"Ошибка сетевого соединения при запросе к API: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка при сохранении погоды: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_and_save_weather())
