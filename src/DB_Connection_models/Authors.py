from run import db


class Authors(db.Model):
    __tablename__ = 'Authors'

    author_id = db.Column(db.Integer, primary_key=True)
    avatar_id = db.Column(db.Integer, db.ForeignKey('Images.image_id'), nullable=True)
    name = db.Column(db.String(50), nullable=True)

    image = db.relationship('Images', lazy=True)
