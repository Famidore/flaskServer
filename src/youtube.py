from googleapiclient.discovery import build
from src.utils import obtain_key


def get_youtube_trending_videos(api_key, region_code="PL", max_results=10):
    youtube = build("youtube", "v3", developerKey=api_key)

    response = (
        youtube.videos()
        .list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results,
        )
        .execute()
    )

    titles = []
    imgs = []
    urls = []

    for video in response["items"]:
        snippet = video["snippet"]
        titles.append(snippet["title"])
        imgs.append(snippet["thumbnails"]["high"]["url"])
        urls.append("https://www.youtube.com/watch?v=" + str(video["id"]))

    return titles, imgs, urls


if __name__ == "__main__":
    get_youtube_trending_videos(obtain_key(file_path="keys.json", mode="youtube_key"))
