from flask import Blueprint, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email

from application import db
from application.models import User


registration_bp = Blueprint('registration_bp', __name__, template_folder="templates", static_folder="static")


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(), Length(max=70)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=60)])
    submit = SubmitField(label='submit')


@registration_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        pw_hash = User.encrypt_password(form.password.data)
        user = User(email=form.email.data, password=pw_hash)
        db.session.add(user)
        db.session.commit()

        return render_template('confirmation.html')

    return render_template('register.html', form=form)