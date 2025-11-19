from yt_api import fetch_channel_details, fetch_videos_for_channel, fetch_comments_for_videos
from processing import process_channel, process_videos, process_comments
from db_insert import insert_channel, insert_videos, insert_comments


def run_pipeline(channel_id):

    raw_channel = fetch_channel_details(channel_id)
    raw_videos = fetch_videos_for_channel(channel_id)
    raw_comments = fetch_comments_for_videos(raw_videos)

    df_channel = process_channel(raw_channel)
    df_videos = process_videos(raw_videos)
    df_comments = process_comments(raw_comments)

    insert_channel(df_channel)
    insert_videos(df_videos)
    insert_comments(df_comments)

    return df_channel, df_videos, df_comments
