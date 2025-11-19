from src.yt_client import get_channel_details, get_video_ids

channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Google Developers channel

print("Channel Details:")
print(get_channel_details(channel_id))

print("\nVideo IDs:")
print(get_video_ids(channel_id)[:5])  # Print first 5 video IDs
