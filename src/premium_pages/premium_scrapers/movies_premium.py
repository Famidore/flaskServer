import requests
from bs4 import BeautifulSoup
import random

movies_url = "https://www.filmweb.pl/films"
series_url = "https://www.filmweb.pl/serials"


def get_movies_items(url: str = movies_url, genre: str = "dramat"):
    # get movies
    pageContent = requests.get(url, timeout=300).text
    soup = BeautifulSoup(pageContent, "html5lib")
    titles = soup.find_all(class_="simplePoster__heading")
    imgs = soup.find_all(class_="simplePoster__image")
    links = soup.find_all(class_="simplePoster__title")

    titles_text = []
    imgs_text = []
    links_text = []

    for i, j, k in zip(titles, imgs, links):

        # check for lazy load
        if i.text not in titles_text and "smartadserver" not in str(k["href"]):
            titles_text.append(i.text)
            imgs_text.append(j["src"])
            links_text.append("https://www.filmweb.pl" + str(k["href"]))

    return titles_text, imgs_text, links_text


def get_movies_premium():
    movies_list, movies_posters, movies_links = get_movies_items(movies_url)
    series_list, series_posters, series_links = get_movies_items(series_url)

    temp = list(
        zip(
            movies_list + series_list,
            movies_posters + series_posters,
            movies_links + series_links,
        )
    )

    random.shuffle(temp)

    media_list, media_posters, media_links = zip(*temp)

    return media_list, media_posters, media_links


if __name__ == "__main__":
    get_movies_premium()
