from sqlalchemy import text
from src.db import engine

query = text("""
INSERT INTO channels (channel_id, channel_name, subscriber_count, video_count, view_count, description)
VALUES ('UC11111', 'Sample Channel', 1000, 10, 5000, 'Testing connection');
""")

with engine.connect() as conn:
    conn.execute(query)
    conn.commit()

print("Data inserted!")
