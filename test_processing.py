from src.yt_client import get_channel_details, get_video_ids, get_video_details, get_comments
from src.data_processing import process_channel_data, process_video_data, process_comment_data

channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers

# Get raw data
raw_channel = get_channel_details(channel_id)
video_ids = get_video_ids(channel_id)[:5]  # first 5 videos
raw_videos = get_video_details(video_ids)
raw_comments = get_comments(video_ids[0])

# Clean data
df_channel = process_channel_data(raw_channel)
df_videos = process_video_data(raw_videos)
df_comments = process_comment_data(raw_comments)

print("\nCHANNEL DF")
print(df_channel)

print("\nVIDEO DF")
print(df_videos.head())

print("\nCOMMENTS DF")
print(df_comments.head())
