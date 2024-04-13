from run import db


class Categories(db.Model):
    __tablename__ = 'Categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=True)
