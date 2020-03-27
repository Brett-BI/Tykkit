from flask import Blueprint, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Length, Email
from flask_login import login_required, login_user, logout_user, current_user

from application.models import User, Ticket, Status, Priority
from application import db, bcrypt
from application import filters
from . import ticket_forms

ticket_bp = Blueprint('ticket_bp', __name__,
                      template_folder='templates',
                      static_folder='static')


@ticket_bp.route('/dashboard')
@login_required
def dashboard():
    print("in dashboard")
    return render_template('dashboard.html')


@ticket_bp.route("/dashboard/me", methods=["GET", "POST"])
@login_required
def my_account():

    form = ticket_forms.AccountInformationForm(obj=current_user)

    if request.method == "POST":
        form.validate_on_submit()

        updated_user = User.query.filter_by(id=current_user.id)
        if updated_user:
            updated_user.update(dict(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data))
        
            db.session.commit()
        else:
            return "Something went wrong updating your information. Sorry about that."

        return redirect(url_for('ticket_bp.my_account'))

    # get account information from flask_login (stores all user information, apparently)
    print(current_user.email)
    print(current_user.id)

    return render_template("my_account.html", user=current_user, form=form)


@ticket_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = ticket_forms.CreateTicketForm()

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
