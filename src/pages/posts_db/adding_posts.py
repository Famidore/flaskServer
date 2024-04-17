import requests
from models import db, Post, Link, ImageLink, Author
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from src.utils import obtain_key

movies_url = "https://www.filmweb.pl/films"
reddit_url = "https://www.reddit.com/"
wykop_trends_url = "https://wykop.pl/k/informacje"


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


def add_authors_to_db(authors):
    for author in authors:
        existing_author = Author.query.filter_by(name=author)
        if existing_author:
            continue
        new_author = Author(author)
        db.session.add(new_author)
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


async def add_reddit_to_db():
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

    add_links_to_db(source_links_text)
    add_imgs_to_db(imgs_links)
    add_authors_to_db(source_text)

    for news, source, link, img, desc in zip(news_text, source_text, source_links_text, imgs_links, descriptions):
        src = Author.query.filter_by(name=source)
        image = ImageLink.query.filter_by(image=img)
        link = Link.query.filter_by(link=link)
        new_reddit_post = Post(news, image.id, link.id, src.id, desc)
        db.session.add(new_reddit_post)
    await db.session.commit()


async def add_wykop_to_db():
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

        imgSoup = BeautifulSoup(str(j), "html5lib")
        img = imgSoup.find("img")
        if str(img["src"]) not in imgs_text:
            imgs_text.append(str(img["src"]))

    add_links_to_db(links_text)
    add_imgs_to_db(imgs_text)

    for title, img, link in zip(titles_text, imgs_text, links_text):
        image = ImageLink.query.filter_by(image=img)
        link = Link.query.filter_by(link=link)
        new_wykop_post = Post(title, image.id, link.id)
        db.session.add(new_wykop_post)
    await db.session.commit()


async def add_youtube_to_db(api_key, region_code="PL", max_results=10):
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
    imgs = []
    urls = []

    for video in response["items"]:
        snippet = video["snippet"]
        titles.append(snippet["title"])
        imgs.append(snippet["thumbnails"]["high"]["url"])
        urls.append("https://www.youtube.com/watch?v=" + str(video["id"]))

    add_links_to_db(urls)
    add_imgs_to_db(imgs)

    for title, img, link in zip(titles, imgs, urls):
        image = ImageLink.query.filter_by(image=img)
        link = Link.query.filter_by(link=link)
        new_youtube_post = Post(title, image.id, link.id)
        db.session.add(new_youtube_post)
    await db.session.commit()


if __name__ == "__main__":
    add_movies_to_db()
    add_reddit_to_db()
    add_wykop_to_db()
    add_youtube_to_db(obtain_key(file_path="keys.json", mode="youtube_key"))
