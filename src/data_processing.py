import pandas as pd
import isodate


# 1️⃣ Convert ISO 8601 duration to seconds ---------------------------
def convert_duration_to_seconds(duration_iso):
    try:
        duration = isodate.parse_duration(duration_iso)
        return int(duration.total_seconds())
    except:
        return None


# 2️⃣ Process channel details ----------------------------------------
def process_channel_data(channel_dict):
    df = pd.DataFrame([channel_dict])
    return df


# 3️⃣ Process video details ------------------------------------------
def process_video_data(video_list, channel_id):
    df = pd.DataFrame(video_list)

    # Add channel_id column (required for SQL foreign key)
    df["channel_id"] = channel_id

    # Convert duration from ISO → seconds
    df["duration_seconds"] = df["duration_iso"].apply(convert_duration_to_seconds)

    # Convert published_at to datetime
    df["published_at"] = pd.to_datetime(df["published_at"])

    return df



# 4️⃣ Process comments ------------------------------------------------
def process_comment_data(comment_list):
    df = pd.DataFrame(comment_list)

    # Convert published_at to datetime
    df["published_at"] = pd.to_datetime(df["published_at"])

    return df
