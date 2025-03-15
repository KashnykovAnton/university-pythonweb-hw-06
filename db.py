import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(dotenv_path=".env")

user = os.getenv("DB_USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
db_name = os.getenv("DB_NAME")

URI = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(URI, echo=False, pool_size=5, max_overflow=0)

SessionLocal = sessionmaker(bind=engine)