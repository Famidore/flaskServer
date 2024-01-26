import requests
from bs4 import BeautifulSoup
from lxml import etree

wykop_trends_url = "https://wykop.pl/k/informacje"


def get_wykop_trends():
    pageContent = requests.get(wykop_trends_url, timeout=300).text
    soup = BeautifulSoup(pageContent, "html5lib")
    titles = soup.find_all("a", class_="heading")
    # imgs = soup.find_all(class_="")
    # links = soup.find_all(class_="heading")

    titles_text = []
    imgs_text = []
    links_text = []

    for i in titles:
        if (i.text) not in titles_text:
            titles_text.append(i.text)
        # if j["src"] not in imgs_text:
        #     imgs_text.append(j["src"])
        # if k["href"] not in links_text:
        #     links_text.append("https://www.filmweb.pl" + str(k["href"]))

    return titles


if __name__ == "__main__":
    print(get_wykop_trends())
