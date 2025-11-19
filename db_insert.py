import pandas as pd
from sqlalchemy import text
from src.db import get_engine

engine = get_engine()


# 1️⃣ Insert channel data --------------------------------------------------
def insert_channel(df_channel):
    with engine.begin() as conn:
        for _, row in df_channel.iterrows():
            conn.execute(text("""
                INSERT INTO channels (channel_id, channel_name, subscriber_count, video_count, view_count, description)
                VALUES (:channel_id, :channel_name, :subscriber_count, :video_count, :view_count, :description)
                ON CONFLICT (channel_id) DO UPDATE SET
                    channel_name = EXCLUDED.channel_name,
                    subscriber_count = EXCLUDED.subscriber_count,
                    video_count = EXCLUDED.video_count,
                    view_count = EXCLUDED.view_count,
                    description = EXCLUDED.description;
            """), row.to_dict())


# 2️⃣ Insert video data ----------------------------------------------------
def insert_videos(df_videos):
    with engine.begin() as conn:
        for _, row in df_videos.iterrows():
            conn.execute(text("""
                INSERT INTO videos (
                    video_id, channel_id, title, description, published_at,
                    view_count, like_count, comment_count, duration_iso, duration_seconds
                )
                VALUES (
                    :video_id, :channel_id, :title, :description, :published_at,
                    :view_count, :like_count, :comment_count, :duration_iso, :duration_seconds
                )
                ON CONFLICT (video_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    description = EXCLUDED.description,
                    view_count = EXCLUDED.view_count,
                    like_count = EXCLUDED.like_count,
                    comment_count = EXCLUDED.comment_count,
                    duration_iso = EXCLUDED.duration_iso,
                    duration_seconds = EXCLUDED.duration_seconds;
            """), row.to_dict())


# 3️⃣ Insert comments -------------------------------------------------------
def insert_comments(df_comments):
    with engine.begin() as conn:
        for _, row in df_comments.iterrows():
            conn.execute(text("""
                INSERT INTO comments (
                    comment_id, video_id, author_name, text, published_at, like_count
                )
                VALUES (
                    :comment_id, :video_id, :author_name, :text, :published_at, :like_count
                )
                ON CONFLICT (comment_id) DO NOTHING;
            """), row.to_dict())
