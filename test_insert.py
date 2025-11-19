from src.yt_client import *
from src.data_processing import *
from src.db_insert import *

channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers

# Fetch raw data
raw_channel = get_channel_details(channel_id)
video_ids = get_video_ids(channel_id)[:3]
raw_videos = get_video_details(video_ids)
raw_comments = get_comments(video_ids[0])

# Clean data
df_channel = process_channel_data(raw_channel)
df_videos = process_video_data(raw_videos, channel_id)

df_comments = process_comment_data(raw_comments)

# Insert into SQL
insert_channel(df_channel)
insert_videos(df_videos)
insert_comments(df_comments)

print("Data inserted successfully!")
