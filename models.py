from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    keyword = db.Column(db.String(256))


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer)
    title = db.Column(db.String(256))
    href = db.Column(db.String(256))