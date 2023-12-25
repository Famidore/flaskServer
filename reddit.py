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
    src_links = soup.find_all("a", class_="block hover:no-underline relative w-[280px]")
    imgs = soup.find_all(
        "img", class_="absolute h-100 w-100 pointer-events-none object-cover m-0"
    )
    descs = soup.find_all(
        "p", class_="truncate text-primary-onBackground text-14 mt-2xs mb-xs"
    )

    news_text = []
    source_text = []
    source_links_text = []
    imgs_links = []
    descriptions = []

    for i, j, k, l, m in zip(news, source, src_links, imgs, descs):
        news_text.append(i.text)
        source_text.append(j.text)
        source_links_text.append("https://www.reddit.com" + str(k["href"]))
        imgs_links.append(str(l["src"]))
        descriptions.append(m.text)

    return news_text, source_text, source_links_text, imgs_links, descriptions


if __name__ == "__main__":
    get_reddit_trends()
