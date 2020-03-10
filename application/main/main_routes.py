from flask import Blueprint, redirect, url_for, render_template


main_bp = Blueprint("main_bp", __name__, template_folder="templates", static_folder="static")


@main_bp.route("/")
def home():

    return render_template("home.html")