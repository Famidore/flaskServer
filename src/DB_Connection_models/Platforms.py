from run import db


class Platforms(db.Model):
    __tablename__ = 'Platforms'

    platform_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
