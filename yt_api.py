import streamlit as st
from googleapiclient.discovery import build


# ---------------------------------------------------------
# Load API key from Streamlit Secrets
# ---------------------------------------------------------
API_KEY = st.secrets["YOUTUBE_API_KEY"]


def get_youtube():
    """Create a YouTube API client using the secret API key."""
    return build("youtube", "v3", developerKey=API_KEY)


# ---------------------------------------------------------
# 1. Fetch Channel Details
# ---------------------------------------------------------
def fetch_channel_details(channel_id):
    youtube = get_youtube()

    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()

    # Fix: Ensure 'items' exists and is not empty
    if not response.get("items"):
        raise Exception("❌ Channel ID not found or API request failed!")

    item = response["items"][0]

    return {
        "channel_id": channel_id,
        "channel_name": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "subscriber_count": int(item["statistics"].get("subscriberCount", 0)),
        "video_count": int(item["statistics"].get("videoCount", 0)),
        "view_count": int(item["statistics"].get("viewCount", 0)),
    }


# ---------------------------------------------------------
# 2. Fetch Videos for a Channel
# ---------------------------------------------------------
def fetch_videos_for_channel(channel_id):
    youtube = get_youtube()

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50,
        order="date"
    )
    response = request.execute()

    if not response.get("items"):
        return []

    videos = []
    for item in response["items"]:
        # Ignore non-video results
        if item["id"].get("kind") != "youtube#video":
            continue

        videos.append({
            "video_id": item["id"]["videoId"],
            "channel_id": channel_id,
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "published_at": item["snippet"]["publishedAt"],
        })

    return videos


# ---------------------------------------------------------
# 3. Fetch Comments for All Videos
# ---------------------------------------------------------
def fetch_comments_for_videos(video_ids):
    youtube = get_youtube()
    comments = []

    for vid in video_ids:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=vid,
                maxResults=50,
                order="relevance",
                textFormat="plainText"
            )
            response = request.execute()

            for item in response.get("items", []):
                top = item["snippet"]["topLevelComment"]["snippet"]

                comments.append({
                    "comment_id": item["id"],
                    "video_id": vid,
                    "author_name": top.get("authorDisplayName", ""),
                    "text": top.get("textDisplay", ""),
                    "published_at": top.get("publishedAt", ""),
                    "like_count": top.get("likeCount", 0)
                })

        except Exception:
            # YouTube often blocks comments on some videos
            continue

    return comments
