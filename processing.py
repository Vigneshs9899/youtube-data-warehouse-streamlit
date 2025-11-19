import pandas as pd
from datetime import datetime, timedelta
import isodate

# ---------------------------------------------------------
# PROCESS CHANNEL DATA
# ---------------------------------------------------------
def process_channel(channel_dict):
    df = pd.DataFrame([channel_dict])
    return df


# ---------------------------------------------------------
# PROCESS VIDEOS
# ---------------------------------------------------------
def process_videos(video_list):

    df = pd.DataFrame(video_list)

    # Convert published_at timestamp
    try:
        df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
    except:
        pass

    # If duration exists, convert ISO8601 → seconds
    if "duration_iso" in df.columns:
        df["duration_seconds"] = df["duration_iso"].apply(
            lambda x: isodate.parse_duration(x).total_seconds() if isinstance(x, str) else None
        )
    else:
        df["duration_seconds"] = None

    return df


# ---------------------------------------------------------
# PROCESS COMMENTS
# ---------------------------------------------------------
def process_comments(comment_list):
    df = pd.DataFrame(comment_list)

    # Convert time
    if "published_at" in df.columns:
        df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")

    return df
