from sqlalchemy.ext.declarative import declarative_base
import os

DB_USER = os.getenv("SERVICE2_DB_USER")
DB_PASSWORD = os.getenv("SERVICE2_DB_PASSWORD")
DB_NAME = os.getenv("SERVICE2_DB_NAME")
DB_HOST = os.getenv("SERVICE2_DB_HOST")
DB_PORT = os.getenv("SERVICE2_DB_PORT")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()
