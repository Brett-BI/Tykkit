from flask import Blueprint, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, Email
from flask_login import login_required, login_user, logout_user, current_user

from application.models import User, Ticket, Status, Priority
from application import db, bcrypt
from application import filters

ticket_bp = Blueprint('ticket_bp', __name__,
                      template_folder='templates',
                      static_folder='static')


def get_ticket_statuses():
    return Status.query.all()


def get_ticket_priorities():
    return Priority.query.all()


class CreateTicketForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=1, max=100)])
    description = TextAreaField('description')
    status = QuerySelectField('status', query_factory=get_ticket_statuses, allow_blank=True, get_label='name')
    priority = QuerySelectField('priority', query_factory=get_ticket_priorities, allow_blank=True, get_label='name')


@ticket_bp.route('/dashboard')
@login_required
def dashboard():
    print("in dashboard")
    return render_template('dashboard.html')


@ticket_bp.route("/me")
@login_required
def my_account():

    # get account information from flask_login (stores all user information, apparently)
    print(current_user.email)   

    return render_template("my_account.html", user=current_user)


@ticket_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = CreateTicketForm()

    if form.validate_on_submit():
        print(request.form.get('status'))
        ticket = Ticket(title=form.title.data, description=form.description.data,
                        priority=request.form.get('priority'), status=request.form.get('status'))
        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for('ticket_bp.dashboard'))

    return render_template('tickets/create.html', form=form)


@ticket_bp.route('/my-application')
@login_required
def my_tickets():
    return render_template('tickets/my-tickets.html')
