from flask import Blueprint
from flask import current_app,  url_for
from flask_login import login_required
from flask import redirect

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

pages = Blueprint('pages', __name__)

@pages.route('/')
def index():
    return redirect(url_for('pages.portal'))

@pages.route('/<path:filename>')
def staticfiles(filename):
    return redirect('static/' + filename)

@login_required
@pages.route('/portal')
def portal():
    return current_app.send_static_file('index.html')








