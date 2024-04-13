from run import db


class Counters(db.Model):
    __tablename__ = 'Counters'

    counter_id = db.Column(db.Integer, primary_key=True)
    view_counter = db.Column(db.Integer, nullable=True, default=0)
    like_counter = db.Column(db.Integer, nullable=True, default=0)
    comment_counter = db.Column(db.Integer, nullable=True, default=0)
    share_counter = db.Column(db.Integer, nullable=True, default=0)
