from .models import db, Post, Link, ImageLink, Author, Platform
from ..youtube import get_youtube_trending_videos
from ..movies import get_movies_list
from ..reddit import get_reddit_trends
from ..wykop import get_wykop_trends


def initialize_platforms():
    platforms = ['youtube', 'wykop', 'reddit', 'filmweb']
    for platform in platforms:
        new_platform = Platform(platform)
        db.session.add(new_platform)
    db.session.commit()

def add_links_to_db(links):
    for link in links:
        existing_link = Link.query.filter_by(link=link).first()
        if existing_link:
            continue
        new_link = Link(link)
        db.session.add(new_link)
    db.session.commit()


def add_imgs_to_db(imgs):
    for img in imgs:
        existing_img = ImageLink.query.filter_by(image=img).first()
        if existing_img:
            continue
        new_img = ImageLink(img)
        db.session.add(new_img)
    db.session.commit()


def add_authors_to_db(authors):
    for author in authors:
        existing_author = Author.query.filter_by(name=author).first()
        if existing_author:
            continue
        new_author = Author(author)
        db.session.add(new_author)
    db.session.commit()


async def add_movies_to_db():
    titles, imgs, links = get_movies_list()

    add_links_to_db(links)
    add_imgs_to_db(imgs)

    for title, img, link in zip(titles, imgs, links):
        image = ImageLink.query.filter_by(image=img).first()
        link = Link.query.filter_by(link=link).first()
        platform = Platform.query.filter_by(name='filmweb').first()
        if image and link:
            new_movie = Post(title=title,
                             image=image.id,
                             link=link.id,
                             platform=platform.id)
            db.session.add(new_movie)
    db.session.commit()


async def add_reddit_to_db():
    news_, sources, source_links, img_links, descriptions = get_reddit_trends()

    for news, source, link, img, desc in zip(news_, sources, source_links, img_links, descriptions):
        src = Author.query.filter_by(name=source).first()
        image = ImageLink.query.filter_by(image=img).first()
        link = Link.query.filter_by(link=link).first()
        platform = Platform.query.filter_by(name='reddit').first()
        if src and image and link:
            new_reddit_post = Post(title=news,
                                   image=image.id,
                                   link=link.id,
                                   author=src.id,
                                   content=desc,
                                   platform=platform.id)
            db.session.add(new_reddit_post)
    db.session.commit()


async def add_wykop_to_db():
    titles, imgs, links = get_wykop_trends()

    add_links_to_db(links)
    add_imgs_to_db(imgs)

    for title, img, link in zip(titles, imgs, links):
        image = ImageLink.query.filter_by(image=img).first()
        link = Link.query.filter_by(link=link).first()
        platform = Platform.query.filter_by(name='wykop').first()
        if image is not None and link is not None:
            new_wykop_post = Post(title=title,
                                  image=image.id,
                                  link=link.id,
                                  platform=platform.id)
            db.session.add(new_wykop_post)
    db.session.commit()

async def add_youtube_to_db(api_key, region_code="PL", max_results=10):
    titles, imgs, urls = get_youtube_trending_videos(api_key, region_code, max_results)

    add_links_to_db(urls)
    add_imgs_to_db(imgs)

    for title, img, link in zip(titles, imgs, urls):
        image = ImageLink.query.filter_by(image=img).first()
        link = Link.query.filter_by(link=link).first()
        platform = Platform.query.filter_by(name='youtube').first()
        if image and link:
            new_youtube_post = Post(title=title,
                                    image=image.id,
                                    link=link.id,
                                    platform=platform.id)
            db.session.add(new_youtube_post)
    db.session.commit()
