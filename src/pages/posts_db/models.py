from ...auth.auth_db.models import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    image_id = db.Column(db.Integer, db.ForeignKey("image_links.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    platform_id = db.Column(db.Integer, db.ForeignKey("platforms.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    counters_id = db.Column(db.Integer, db.ForeignKey("counters.id"))
    link_id = db.Column(db.Integer, db.ForeignKey("links.id"))
    title = db.Column(db.String)
    content = db.Column(db.String)
    added_date = db.Column(db.DateTime)

    def __init__(self, title, image, link, author=None, content=None):
        self.title = title
        self.image_id = image
        self.link_id = link
        self.author_id = author
        self.content = content

class Counter(db.Model):
    __tablename__ = "counters"

    id = db.Column(db.Integer, primary_key=True)
    view_counter = db.Column(db.Integer)
    like_counter = db.Column(db.Integer)
    comment_counter = db.Column(db.Integer)
    share_counter = db.Column(db.Integer)


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String)
    name = db.Column(db.String)

    def __init__(self, name):
        self.name = name

class Link(db.Model):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)

    def __init__(self, link):
        self.link = link


class Platform(db.Model):
    __tablename__ = "platforms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)

class ImageLink(db.Model):
    __tablename__ = "image_links"

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)

    def __init__(self, image):
        self.image = image