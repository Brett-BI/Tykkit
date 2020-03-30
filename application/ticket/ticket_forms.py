from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, Email

from application.models import User, Ticket, Status, Priority
from application import db, bcrypt


def get_ticket_statuses():
    return Status.query.all()


def get_ticket_priorities():
    return Priority.query.all()


class CreateTicketForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=1, max=100)])
    description = TextAreaField('description')
    status = QuerySelectField('status', query_factory=get_ticket_statuses, allow_blank=True, get_label='name')
    priority = QuerySelectField('priority', query_factory=get_ticket_priorities, allow_blank=True, get_label='name')


class AccountInformationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=1, max=100)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=40)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=64)])
