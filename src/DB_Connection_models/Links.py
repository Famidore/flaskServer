from run import db


class Links(db.Model):
    __tablename__ = 'Links'

    link_id = db.Column(db.Integer, primary_key=True)
    link_type = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(50), nullable=False)
