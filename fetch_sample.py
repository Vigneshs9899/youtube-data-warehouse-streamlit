from sqlalchemy import text
from src.db import engine

query = text("SELECT * FROM channels;")

with engine.connect() as conn:
    result = conn.execute(query).fetchall()
    print(result)
