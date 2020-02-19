from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from sqlalchemy.orm import relationship
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, Email
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(70), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


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



# forms
class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(), Length(max=70)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=60)])


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(), Length(max=70)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=60)])


def get_ticket_statuses():
    return Status.query.all()


def get_ticket_priorities():
    return Priority.query.all()


class CreateTicketForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=1, max=100)])
    description = TextAreaField('description')
    status = QuerySelectField('status', query_factory=get_ticket_statuses, allow_blank=True, get_label='name')
    priority = QuerySelectField('priority', query_factory=get_ticket_priorities, allow_blank=True, get_label='name')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data.encode('utf-8')):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
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

        return '<p>registered. thanks.</p><p>email: {}, password: {}'.format(form.email.data, form.password.data)

    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = CreateTicketForm()

    if form.validate_on_submit():
        #get the ids from the database
        # _status = Status.query.filter_by(name=form.status.data).one()
        # print(_status.id)
        #
        # _priority = Priority.query.filter_by(name=form.priority.data).one()
        # print(_priority.id)

        print(request.form.get('status'))
        ticket = Ticket(title=form.title.data, description=form.description.data,
                        priority=request.form.get('priority'), status=request.form.get('status'))
        db.session.add(ticket)
        db.session.commit()
        #flash('p: {} ::: s: {}'.format(form.priority.data, form.status.data))

        return redirect(url_for('dashboard'))

    return render_template('tickets/create.html', form=form)


@app.route('/my-tickets')
@login_required
def my_tickets():
    return render_template('tickets/my-tickets.html')


if __name__ == '__main__':
    app.run(debug=True)
