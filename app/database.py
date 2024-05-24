import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings


load_dotenv()

# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@postgresserver/dbname"
SQLALCHEMY_DATABASE_URL = \
    f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#create db dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()