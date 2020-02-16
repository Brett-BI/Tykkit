from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)