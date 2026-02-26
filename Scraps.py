from googleapiclient.discovery import build
import pandas as pd

# API KEY & VIDEO ID
api_key = "-"
video_id = "lTKZ2m9YJms"

youtube = build("youtube", "v3", developerKey=api_key)

data = []

request = youtube.commentThreads().list(
    part="snippet,replies",
    videoId=video_id,
    maxResults=100,
    textFormat="plainText"
)

response = request.execute()

while request:
    for item in response["items"]:
        top_comment = item["snippet"]["topLevelComment"]
        snippet = top_comment["snippet"]

        # KOMENTAR UTAMA
        data.append({
            "video_id": video_id,
            "comment_id": top_comment["id"],
            "parent_id": None,
            "type": "comment",
            "create_time": pd.to_datetime(snippet["publishedAt"]).timestamp(),
            "create_time_iso": snippet["publishedAt"],
            "username": snippet["authorDisplayName"],
            "text": snippet["textDisplay"],
            "like_count": snippet["likeCount"],
            "reply_count": item["snippet"]["totalReplyCount"]
        })

        # REPLY
        if "replies" in item:
            for reply in item["replies"]["comments"]:
                r = reply["snippet"]

                data.append({
                    "video_id": video_id,
                    "comment_id": reply["id"],
                    "parent_id": r["parentId"],
                    "type": "reply",
                    "create_time": pd.to_datetime(r["publishedAt"]).timestamp(),
                    "create_time_iso": r["publishedAt"],
                    "username": r["authorDisplayName"],
                    "text": r["textDisplay"],
                    "like_count": r["likeCount"],
                    "reply_count": None
                })

    request = youtube.commentThreads().list_next(request, response)
    if request:
        response = request.execute()

df = pd.DataFrame(data)
df = df.sort_values(by="create_time")
df.reset_index(drop=True, inplace=True)

df.to_csv("dataset_youtube_lTKZ2m9YJms.csv", index=False)

print("Total data:", len(df))
