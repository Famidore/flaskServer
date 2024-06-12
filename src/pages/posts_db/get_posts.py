from .models import Post, Link, ImageLink, Author, Platform
from src.utils import translate_media_name


def get_posts(platform_name, amount=10):
    # platform_name = translate_media_name(platform_name)
    titles = []
    images = []
    links = []
    platform = Platform.query.filter_by(name=platform_name).first()
    posts = (
        Post.query.filter_by(platform_id=platform.id)
        .order_by(Post.added_date.desc())
        .limit(amount)
        .all()
    )
    if platform_name == "reddit":
        authors = []
        contents = []
        for post in posts:
            titles.append(post.title)
            image = ImageLink.query.filter_by(id=post.image_id).first()
            images.append(image.image)
            link = Link.query.filter_by(id=post.link_id).first()
            links.append(link.link)
            author = Author.query.filter_by(id=post.author_id).first()
            authors.append(author.name)
            contents.append(post.content)
        return titles, authors, links, images, contents
    else:
        for post in posts:
            titles.append(post.title)
            image = ImageLink.query.filter_by(id=post.image_id).first()
            images.append(image.image)
            link = Link.query.filter_by(id=post.link_id).first()
            links.append(link.link)
        return titles, images, links


if __name__ == "__main__":
    get_posts()
