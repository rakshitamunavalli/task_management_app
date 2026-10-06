from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utils.settings import Settings

Base = declarative_base()

engine= create_engine(url=Settings.DB_CONNECTION)

Localsession = sessionmaker(bind=engine)

def get_db():
    session = Localsession()
    try:
        yield session
    finally:
        session.close()
