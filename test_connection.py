from src.db import engine

try:
    conn = engine.connect()
    print("🎉 Connection to PostgreSQL successful!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
