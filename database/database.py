from sqlalchemy import create_engine,Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3

engine = create_engine("sqlite:///weather_data.db", echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()