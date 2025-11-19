from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

# Create YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)


# 1️⃣ GET CHANNEL DETAILS ----------------------------------------------------
def get_channel_details(channel_id):
    request = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        id=channel_id
    )
    response = request.execute()

    if "items" not in response or len(response["items"]) == 0:
        return None

    data = response["items"][0]

    channel_info = {
        "channel_id": channel_id,
        "channel_name": data["snippet"]["title"],
        "description": data["snippet"]["description"],
        "subscriber_count": int(data["statistics"].get("subscriberCount", 0)),
        "view_count": int(data["statistics"].get("viewCount", 0)),
        "video_count": int(data["statistics"].get("videoCount", 0)),
        "playlist_id": data["contentDetails"]["relatedPlaylists"]["uploads"]
    }

    return channel_info


# 2️⃣ GET ALL VIDEO IDS FROM CHANNEL ----------------------------------------
def get_video_ids(channel_id):
    playlist_id = get_channel_details(channel_id)["playlist_id"]

    video_ids = []
    next_page = None

    while True:
        req = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page
        )
        res = req.execute()

        for item in res["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        next_page = res.get("nextPageToken")

        if not next_page:
            break

    return video_ids


# 3️⃣ GET VIDEO DETAILS ------------------------------------------------------
def get_video_details(video_ids):
    video_data = []

    for i in range(0, len(video_ids), 50):
        req = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(video_ids[i:i+50])
        )
        res = req.execute()

        for item in res["items"]:
            data = {
                "video_id": item["id"],
                "title": item["snippet"]["title"],
                "description": item["snippet"].get("description"),
                "published_at": item["snippet"]["publishedAt"],
                "view_count": int(item["statistics"].get("viewCount", 0)),
                "like_count": int(item["statistics"].get("likeCount", 0)),
                "comment_count": int(item["statistics"].get("commentCount", 0)),
                "duration_iso": item["contentDetails"]["duration"],
            }
            video_data.append(data)

    return video_data


# 4️⃣ GET COMMENTS FOR A VIDEO ----------------------------------------------
def get_comments(video_id):
    comments_list = []
    next_page = None

    while True:
        req = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=50,
            pageToken=next_page,
            textFormat="plainText"
        )
        res = req.execute()

        for item in res["items"]:
            top_comment = item["snippet"]["topLevelComment"]
            snippet = top_comment["snippet"]

            comment_info = {
                "comment_id": top_comment["id"],
                "video_id": video_id,
                "author_name": snippet.get("authorDisplayName"),
                "text": snippet.get("textDisplay"),
                "published_at": snippet.get("publishedAt"),
                "like_count": snippet.get("likeCount")
            }
            comments_list.append(comment_info)

        next_page = res.get("nextPageToken")
        if not next_page:
            break

    return comments_list
