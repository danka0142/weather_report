import asyncio                                   
from sqlalchemy import URL, text                   
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from os import getenv

load_dotenv()
API_KEY = getenv("API_KEY")

#обьявляем подключение к базе и создаём асинхронный движок

url_object = URL.create(
    drivername = "postgresql+asyncpg",
    username = getenv("postgre_login"),
    password = getenv("postgre_pwd"),
    host = getenv("postgre_ip"),
    port = getenv("postgre_port", 5432),
    database = "WeatherDB"
)

async_engine = create_async_engine(url_object)

async def check_connection():
    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"Успешное подключение! Результат: {result.scalar()}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    finally:
        await async_engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_connection())
