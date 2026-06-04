
from database import async_engine
from datetime import datetime
from sqlalchemy import Numeric, Integer, Float, String, DateTime, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import asyncio

#обьявляем модель данных и создаем табличку

class Base(DeclarativeBase):
    pass

class WeatherData(Base):
    __tablename__ = "weather_history"
    __table_args__ = (
        CheckConstraint("lat BETWEEN -90 AND 90", name="chk_lat_range"),
        CheckConstraint("lon BETWEEN -180 AND 180", name="chk_lon_range"),
        {"schema": "stg"}  # Ваша схема в PostgreSQL
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Географические данные
    lat: Mapped[float] = mapped_column(Numeric(8, 6), nullable=False)
    lon: Mapped[float] = mapped_column(Numeric(9, 6), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Основные параметры погоды
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    feels_like: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[int] = mapped_column(Integer, nullable=False)  # В процентах (0-100)
    pressure: Mapped[int] = mapped_column(Integer, nullable=False)  # В гПа (hPa)
    
    # Ветер и облачность
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    wind_deg: Mapped[int] = mapped_column(Integer, nullable=False)  # Направление в градусах
    clouds: Mapped[int] = mapped_column(Integer, nullable=False)    # Облачность в %
    visibility: Mapped[int] = mapped_column(Integer, nullable=False) # Видимость в метрах
    
    # Время (из Unix timestamp в datetime)
    sunrise: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sunset: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Текстовое описание и иконка
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    icon: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Системное поле: когда запись была внесена в вашу БД
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы успешно созданы в схеме stg!")

if __name__ == "__main__":
    asyncio.run(init_db())

