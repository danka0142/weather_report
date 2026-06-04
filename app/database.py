from sqlalchemy import URL
from sqlalchemy import create_engine
#import pyodbc
from dotenv import load_dotenv
from os import getenv
load_dotenv()
API_KEY =getenv("API_KEY")

url_object = URL.create(
    drivername = "postgresql+psycopg2",
    username = getenv("postgre_login"),
    password = getenv("postgre_pwd"),
    host = getenv("postgre_ip"),
    port = getenv("postgre_port", 5432),
    database = "WeatherDB"
)

engine = create_engine(url_object)

