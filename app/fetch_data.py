import asyncio
from sqlalchemy import select
# Используем sessionmaker для совместимости с SQLAlchemy 1.4+
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

import database
from model import WeatherData

# Настройка фабрики сессий
Session = sessionmaker(
    bind=database.async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def fetch_all_weather():
    try:
        async with Session() as session:
            # Формируем запрос: SELECT * FROM stg.weather_history
            query = select(WeatherData).order_by(WeatherData.created_at.desc())
            
            # Выполняем асинinternal запрос
            result = await session.execute(query)
            
            # Извлекаем все объекты (строки) из результата
            records = result.scalars().all()
            
            if not records:
                print("В таблице weather_history пока нет записей.")
                return
                
            print(f"--- Всего найдено записей: {len(records)} ---")
            for row in records:
                print(
                    f"[{row.created_at}] ID: {row.id} | "
                    f"Координаты: {row.lat}, {row.lon} | "
                    f"Темп: {row.temperature}°C (Ощущается как: {row.feels_like}°C) | "
                    f"Погода: {row.description}"
                )
                
    except Exception as e:
        print(f"Ошибка при чтении данных из БД: {e}")
    finally:
        # Закрываем пул соединений при завершении работы скрипта
        await database.async_engine.dispose()

if __name__ == "__main__":
    asyncio.run(fetch_all_weather())
