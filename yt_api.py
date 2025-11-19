import os
import googleapiclient.discovery
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube():
    return googleapiclient.discovery.build(
        "youtube", "v3", developerKey=API_KEY
    )

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

    if not response["items"]:
        raise Exception("Channel ID not found!")

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
# 2. Fetch Videos
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

    videos = []
    for item in response["items"]:
        if item["id"]["kind"] != "youtube#video":
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
        except:
            continue

    return comments
