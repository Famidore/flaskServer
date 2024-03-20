import requests
from bs4 import BeautifulSoup

wykop_trends_url = "https://wykop.pl/k/informacje"


def get_wykop_trends():
    pageContent = requests.get(wykop_trends_url, timeout=300).text
    beginSoup = BeautifulSoup(pageContent, "html5lib")
    content = beginSoup.find(
        class_="stream category-stream from-pagination-category-stream"
    )
    soup = BeautifulSoup(str(content), "html5lib")
    titles = soup.find_all("h2", class_="heading")
    imgs = soup.find_all("figure", class_="")
    # links = soup.find_all(class_="heading")

    titles_text = []
    imgs_text = []
    links_text = []

    for i, j in zip(titles, imgs):
        titleSoup = BeautifulSoup(i.text, "html5lib")
        title = titleSoup.find(class_="")
        if (title.text.strip()) not in titles_text:
            titles_text.append(title.text.strip())

        linksSoup = BeautifulSoup(str(i), "html5lib")
        link = linksSoup.find("a")
        if ("https://wykop.pl" + str(link["href"])) not in links_text:
            links_text.append("https://wykop.pl" + str(link["href"]))

        # fix issues about missing images

        imgSoup = BeautifulSoup(str(j), "html5lib")
        img = imgSoup.find("img")
        if str(img["src"]) not in imgs_text:
            imgs_text.append(str(img["src"]))

    return titles_text, imgs_text, links_text


if __name__ == "__main__":
    x2, y2, z2 = get_wykop_trends()
    for x, y, z in zip(x2, y2, z2):
        print(f"\n\n{x} \n {y} \n {z} \n\n")
