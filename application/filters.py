from flask import Flask, Blueprint

filters = Blueprint("filters", __name__)


@filters.app_template_filter()
def datetimeformat(value, format="%H:%M / %d-%m-%Y"):
    return value.strftime(format)