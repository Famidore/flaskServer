from run import db


class Posts(db.Model):
    __tablename__ = 'Posts'

    post_id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('Images.image_id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('Authors.author_id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('Platforms.platform_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'), nullable=False)
    counters_id = db.Column(db.Integer, db.ForeignKey('Counters.counter_id'), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('Links.link_id'), nullable=False)
    content = db.Column(db.String(50), nullable=True)
    added_date = db.Column(db.DateTime, nullable=False)

    image = db.relationship('Images', lazy=True)
    author = db.relationship('Authors', lazy=True)
    platform = db.relationship('Platforms', lazy=True)
    category = db.relationship('Categories', lazy=True)
    counters = db.relationship('Counters', lazy=True)
    link = db.relationship('Links', lazy=True)
