from flask import Blueprint,render_template, redirect, url_for, request, flash


errors = Blueprint('errors',__name__, template_folder='templates',static_folder='static',static_url_path='/error/static')


@errors.app_errorhandler(404)
def error_404(error):
	return render_template('error.html'),404


@errors.app_errorhandler(403)
def error_403(error):
	return render_template('error.html'),403


@errors.app_errorhandler(500)
def error_500(error):
	return render_template('error.html'),500