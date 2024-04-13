from run import db


class Images(db.Model):
    __tablename__ = 'Images'

    image_id = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.String(50), nullable=True)
