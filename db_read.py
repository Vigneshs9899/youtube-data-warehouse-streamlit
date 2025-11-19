import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

# Read Supabase/PostgreSQL connection URL from Streamlit Secrets
engine = create_engine(st.secrets["DATABASE_URL"])

def load_channels():
    return pd.read_sql("SELECT * FROM channels ORDER BY channel_name;", engine)

def load_videos(channel_id=None):
    if channel_id:
        query = f"SELECT * FROM videos WHERE channel_id = '{channel_id}' ORDER BY published_at DESC;"
    else:
        query = "SELECT * FROM videos ORDER BY published_at DESC;"
    return pd.read_sql(query, engine)

def load_comments(video_id=None):
    if video_id:
        query = f"SELECT * FROM comments WHERE video_id = '{video_id}' ORDER BY published_at DESC;"
    else:
        query = "SELECT * FROM comments ORDER BY published_at DESC;"
    return pd.read_sql(query, engine)
