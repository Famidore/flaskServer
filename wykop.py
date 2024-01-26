import requests
from bs4 import BeautifulSoup
from lxml import etree

wykop_trends_url = "https://wykop.pl/k/informacje"


def get_wykop_trends():
    pageContent = requests.get(wykop_trends_url, timeout=300).text
    soup = BeautifulSoup(pageContent, "html5lib")
    titles = soup.find_all("h2", class_="heading")
    # imgs = soup.find_all(class_="")
    # links = soup.find_all(class_="heading")

    titles_text = []
    imgs_text = []
    links_text = []

    for i in titles:
        titleSoup = BeautifulSoup(i.text, "html5lib")
        title = titleSoup.find(class_="")
        if (title.text.strip()) not in titles_text:
            titles_text.append(title.text.strip())

    return titles_text


if __name__ == "__main__":
    for i in get_wykop_trends():
        print(i)
