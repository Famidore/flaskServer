import requests
from bs4 import BeautifulSoup

reddit_url = "https://www.reddit.com/"


def get_reddit_trends():
    pageContent = requests.get(reddit_url, timeout=300).text
    soup = BeautifulSoup(pageContent, "html5lib")
    news = soup.find_all(
        class_="truncate font-bold text-primary-onBackground text-24 m-0"
    )
    source = soup.find_all(class_="font-bold mr-2xs ml-xs")
    return news, source
