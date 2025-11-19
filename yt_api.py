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

    # 1️⃣ First request: list videos
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=50,
        order="date"
    )
    response = request.execute()

    video_ids = [
        item["id"]["videoId"]
        for item in response.get("items", [])
        if item["id"]["kind"] == "youtube#video"
    ]

    if not video_ids:
        return []

    # 2️⃣ Second request: get full video details
    request2 = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=",".join(video_ids)
    )
    response2 = request2.execute()

    videos = []

    for item in response2.get("items", []):
        snippet = item["snippet"]
        stats = item.get("statistics", {})
        content = item.get("contentDetails", {})

        # Convert duration ISO8601 → seconds
        from isodate import parse_duration
        try:
            duration_seconds = int(parse_duration(content.get("duration", "PT0S")).total_seconds())
        except:
            duration_seconds = None

        videos.append({
            "video_id": item["id"],
            "channel_id": channel_id,
            "title": snippet["title"],
            "description": snippet.get("description", ""),
            "published_at": snippet.get("publishedAt"),
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
            "comment_count": int(stats.get("commentCount", 0)),
            "duration_iso": content.get("duration", "PT0S"),
            "duration_seconds": duration_seconds
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
