from sqlalchemy.orm import relationship
from flask_login import UserMixin
import datetime

from application import db, login_manager, bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(70), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    @staticmethod
    def encrypt_password(password):
        pw = bcrypt.generate_password_hash(password)

        return pw.decode("utf-8")


    @staticmethod
    def check_password(self, db_password, form_password):

        return bcrypt.check_password_hash(db_password, form_password.data.encode('utf-8'))


class Status(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    ticket = relationship("Ticket", back_populates="status", uselist=False)

    def __repr__(self):
        return self.name


class Ticket(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    creation_datetime = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    status_id = db.Column(db.Integer(), db.ForeignKey('status.id'), nullable=False)
    priority_id = db.Column(db.Integer(),db.ForeignKey('priority.id'), nullable=False)

    status = relationship("Status", back_populates="ticket")
    priority = relationship("Priority", back_populates="ticket")


class Priority(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    ticket = relationship("Ticket", back_populates="priority", uselist=False)

    def __repr__(self):
        return self.name

