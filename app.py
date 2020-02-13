from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'bigolesecret'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# models
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(70), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

# forms
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=50)])
    email = StringField('email', validators=[InputRequired(), Email(), Length(max=70)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=60)])

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return 'username: {}, password: {}, and email: {}'.format(form.username.data, form.password.data, form.email.data)
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
