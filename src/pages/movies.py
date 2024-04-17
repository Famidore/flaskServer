import requests
from bs4 import BeautifulSoup

movies_url = "https://www.filmweb.pl/films"


def get_movies_list():
    pageContent = requests.get(movies_url, timeout=300).text
    soup = BeautifulSoup(pageContent, "html5lib")
    titles = soup.find_all(class_="simplePoster__heading")
    imgs = soup.find_all(class_="simplePoster__image")
    links = soup.find_all(class_="simplePoster__title")

    titles_text = []
    imgs_text = []
    links_text = []

    for i, j, k in zip(titles, imgs, links):

        # check for lazy load
        if i.text not in titles_text:
            titles_text.append(i.text)
            imgs_text.append(j["src"])
            links_text.append("https://www.filmweb.pl" + str(k["href"]))

    return titles_text, imgs_text, links_text


if __name__ == "__main__":
    get_movies_list()
