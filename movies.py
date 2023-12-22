import requests
from bs4 import BeautifulSoup

movies_url = "https://www.filmweb.pl/films"


def get_movies_list():
    pageContent = requests.get(movies_url, timeout=300).text
    soup = BeautifulSoup(pageContent, "html5lib")
    titles = soup.find_all(class_="simplePoster__heading")
    return titles
