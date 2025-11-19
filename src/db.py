import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load DATABASE_URL from Streamlit Secrets (Neon DB)
DATABASE_URL = st.secrets["DATABASE_URL"]

# Create engine using Neon connection
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)

def get_engine():
    return engine

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
