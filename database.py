import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure pg8000 is used instead of psycopg2
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://insurance_db_nz57_user:4PMTxlKA1MhJuL0e5DwaQjPuj0WC3e9D@dpg-d3dvnbjipnbc73bel2k0-a.oregon-postgres.render.com/insurance_db_nz57")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
