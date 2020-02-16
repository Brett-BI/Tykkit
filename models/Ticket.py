from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy

class Ticket(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    creation_datetime = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    status = db.Column(db.Integer(), nullable=False)
    priority = db.Column(db.Integer(), nullable=False)