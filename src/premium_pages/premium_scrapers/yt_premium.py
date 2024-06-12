from googleapiclient.discovery import build
import itertools
from src.utils import obtain_key


def returnYoutubeInfo(
    api_key: str,
    region_code: str = "PL",
    max_results: int = 10,
    videoCategory: str = "",
):
    youtube = build("youtube", "v3", developerKey=api_key)

    response = (
        youtube.videos()
        .list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results,
            videoCategoryId=videoCategory,
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


def get_youtube_premium_objects(
    api_key: str,
    videoCategories: list = [],
    max_results: int = 10,
    region_code: str = "PL",
):
    if videoCategories:
        titles = []
        imgs = []
        urls = []
        for i in videoCategories:
            title, img, url = returnYoutubeInfo(
                api_key=api_key, max_results=max_results, videoCategory=str(i)
            )
            for i, j, k in zip(title, img, url):
                titles.append(i)
                imgs.append(j)
                urls.append(k)
        return titles, imgs, urls


if __name__ == "__main__":
    print(
        list(
            itertools.chain(
                *get_youtube_premium_objects(
                    obtain_key(file_path="CONFIG.json", mode="youtube_key"),
                    videoCategories=[2, 10],
                )
            )
        )
    )
