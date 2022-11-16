from flask import Blueprint, render_template

errors = Blueprint('error',__name__)

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'),500