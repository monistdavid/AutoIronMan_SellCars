import datetime
from db_model.db_connection import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now())
