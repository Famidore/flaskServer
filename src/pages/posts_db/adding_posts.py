import requests
from models import db, Post, Link, ImageLink
from bs4 import BeautifulSoup

movies_url = "https://www.filmweb.pl/films"


def add_links_to_db(links):
    for link in links:
        existing_link = Link.query.filter_by(link=link)
        if existing_link:
            continue
        new_link = Link(link)
        db.session.add(new_link)
    db.session.commit()


def add_imgs_to_db(imgs):
    for img in imgs:
        existing_img = Link.query.filter_by(image=img)
        if existing_img:
            continue
        new_img = ImageLink(img)
        db.session.add(new_img)
    db.session.commit()


async def add_movies_to_db():
    pageContent = requests.get(movies_url, timeout=300).text
    soup = BeautifulSoup(pageContent, "html5lib")
    titles = soup.find_all(class_="simplePoster__heading")
    imgs = soup.find_all(class_="simplePoster__image")
    links = soup.find_all(class_="simplePoster__title")

    titles_text = []
    imgs_text = []
    links_text = []

    for i, j, k in zip(titles, imgs, links):
        if (i.text) not in titles_text:
            titles_text.append(i.text)
        if j["src"] not in imgs_text:
            imgs_text.append(j["src"])
        if k["href"] not in links_text:
            links_text.append("https://www.filmweb.pl" + str(k["href"]))

    add_links_to_db(links_text)
    add_imgs_to_db(imgs_text)

    for title, img, link in zip(titles_text, imgs_text, links_text):
        image = ImageLink.query.filter_by(image=img)
        link = Link.query.filter_by(link=link)
        new_movie = Post(title, image.id, link.id)
        db.session.add(new_movie)
    await db.session.commit()


if __name__ == "__main__":
    add_movies_to_db()
