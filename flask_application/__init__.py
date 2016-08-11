import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask
from flask_login import LoginManager
from flask_limiter import Limiter
from flask import redirect
from utils.tasks import make_celery
import logging

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

FLASK_APP_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(FLASK_APP_DIR, '..', 'templates'),
    static_folder=os.path.join(FLASK_APP_DIR, '..', 'static')
)

# Config
app.config.from_object('flask_application.config.app_config')

# Redis store
from flask_application.database.portaldb import db
app.db = db
app.db.init_app(app)

# Celery task queue
celery = make_celery(app)

# Rate limiter
limiter = Limiter(app, global_limits=["10000 per hour"])

# Manage logins
def unauthorized_handler():
    return redirect(app.config['MY_URL'], 401)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.unauthorized_handler(unauthorized_handler)

# Logging
app.logger.setLevel(logging.INFO)
from flask_application.log import applogger
applogger.register_logging(app)

from flask_application.files.controllers import files
app.register_blueprint(files)
from flask_application.users.controllers import users
app.register_blueprint(users)
#from flask_application.auth.controllers import auth
#app.register_blueprint(auth)
from flask_application.source.controllers import source
app.register_blueprint(source)
from flask_application.admin.controllers import admin
app.register_blueprint(admin)

if app.debug:
    app.logger.info("Debug mode. Serving pages")
    from flask_application.pages.controllers import pages
    app.register_blueprint(pages)
else:
    app.logger.info("Production mode. Not serving pages")


# Connectors
from flask_application.source.w2ewithings.controllers import source as w2ewithings
app.register_blueprint(w2ewithings)
from flask_application.source.w2emoves.controllers import source as w2emoves
app.register_blueprint(w2emoves)

