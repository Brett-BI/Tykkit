from flask import Blueprint, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email
from flask_login import login_user, logout_user

from application import login_manager
from application.models import User


auth_bp = Blueprint("auth_bp", __name__, template_folder="templates", static_folder="static")


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(), Length(max=70)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=60)])
    submit = SubmitField(label='submit')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print("in auth bp")

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(db_password=user.password, form_password=form.password.data.encode('utf-8')):
            print("login success")
            login_user(user)
            return redirect(url_for('ticket_bp.dashboard'))
        else:
            print("login failure")
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
