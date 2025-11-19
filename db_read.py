import pandas as pd
import sqlalchemy
import os

# Read DATABASE_URL from environment (Streamlit Secrets in cloud)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found — set it in Streamlit Secrets!")

# Create engine
engine = sqlalchemy.create_engine(DATABASE_URL, pool_pre_ping=True)


def load_channels():
    query = "SELECT * FROM channels ORDER BY channel_name;"
    return pd.read_sql(query, engine)


def load_videos(channel_id=None):
    if channel_id:
        query = f"""
            SELECT * FROM videos
            WHERE channel_id = '{channel_id}'
            ORDER BY published_at DESC;
        """
    else:
        query = "SELECT * FROM videos ORDER BY published_at DESC;"
    return pd.read_sql(query, engine)


def load_comments(video_id=None):
    if video_id:
        query = f"""
            SELECT * FROM comments
            WHERE video_id = '{video_id}'
            ORDER BY published_at DESC;
        """
    else:
        query = "SELECT * FROM comments ORDER BY published_at DESC;"
    return pd.read_sql(query, engine)
