from flask import Blueprint, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, Email
from flask_login import login_required, login_user, logout_user

from application.models import User, Ticket, Status, Priority
from application import db, bcrypt


ticket_bp = Blueprint('ticket_bp', __name__,
                       template_folder='templates',
                       static_folder='static')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(), Length(max=70)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=60)])
    submit = SubmitField(label='submit')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(), Length(max=70)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=60)])
    submit = SubmitField(label='submit')


def get_ticket_statuses():
    return Status.query.all()


def get_ticket_priorities():
    return Priority.query.all()


class CreateTicketForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=1, max=100)])
    description = TextAreaField('description')
    status = QuerySelectField('status', query_factory=get_ticket_statuses, allow_blank=True, get_label='name')
    priority = QuerySelectField('priority', query_factory=get_ticket_priorities, allow_blank=True, get_label='name')


@ticket_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data.encode('utf-8')):
            login_user(user)
            return redirect(url_for('ticket_bp.dashboard'))
        else:
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@ticket_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print(form.password.data)
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        print(pw_hash)
        print(pw_hash.decode('utf-8'))
        user = User(email=form.email.data, password=pw_hash.decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return render_template('confirmation.html')
    return render_template('register.html', form=form)


@ticket_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('ticket_bp.login'))


@ticket_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


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

