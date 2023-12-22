from googleapiclient.discovery import build


def obtain_key():
    file_path = "api_key.txt"
    try:
        with open(file_path, "r") as file:
            api_key = file.read()
    except FileNotFoundError:
        api_key = ""
        f = open(file_path, "a")
        print("\nEnter your api key in the 'api_key.txt' file")
    except Exception as e:
        api_key = ""
        print(f"An error occurred: {e}")
    return api_key


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
    for video in response["items"]:
        snippet = video["snippet"]
        titles.append(snippet["title"])
    return titles


get_youtube_trending_videos(obtain_key())
