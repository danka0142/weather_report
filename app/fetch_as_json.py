import asyncio
import json
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

import database
from model import WeatherData

Session = sessionmaker(
    bind=database.async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def fetch_latest_weather_json():
    try:
        async with Session() as session:
            # Сортируем по убыванию времени и берем ровно 1 запись
            query = select(WeatherData).order_by(WeatherData.created_at.desc()).limit(1)
            
            result = await session.execute(query)
            # scalar() вернет один объект WeatherData или None, если таблица пуста
            row = result.scalar()
            
            if not row:
                print("В таблице weather_history пока нет записей.")
                return None
                
            # Формируем структуру словаря (JSON)
            weather_json = {
                "id": row.id,
                "coordinates": {
                    "lat": float(row.lat),  # Конвертируем Numeric/Decimal в float для JSON
                    "lon": float(row.lon)
                },
                "timezone": row.timezone,
                "weather": {
                    "temperature": row.temperature,
                    "feels_like": row.feels_like,
                    "humidity": row.humidity,
                    "pressure": row.pressure
                },
                "wind": {
                    "speed": row.wind_speed,
                    "deg": row.wind_deg
                },
                "clouds": row.clouds,
                "visibility": row.visibility,
                "astronomy": {
                    "sunrise": row.sunrise.isoformat(),  # Переводим datetime в строку ISO
                    "sunset": row.sunset.isoformat()
                },
                "info": {
                    "description": row.description,
                    "icon": row.icon
                },
                "created_at": row.created_at.isoformat()
            }
            
            # Если нужна именно строка JSON для вывода или отправки:
            json_string = json.dumps(weather_json, ensure_ascii=False, indent=4)
            print(json_string)
            
            return weather_json
                
    except Exception as e:
        print(f"Ошибка при чтении данных из БД: {e}")
        return None
    finally:
        await database.async_engine.dispose()

if __name__ == "__main__":
    asyncio.run(fetch_latest_weather_json())
