import logging
from flask import request, jsonify
from logging.handlers import SMTPHandler
from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask_application.utils.client import get_client_ip
import datetime
from werkzeug.exceptions import HTTPException
from flask_login import current_user

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"


def register_logging(app):
    if not app.debug and not app.testing:
        mail_handler = SMTPHandler(mailhost=app.config['MAIL_SERVER'],
                                   fromaddr='server-error@' + app.config['SERVER_NAME'],
                                   toaddrs=app.config['SYS_ADMINS'], subject='Application error at server ' + app.config['SERVER_NAME'],
                                   credentials=app.config['MAIL_CREDENTIALS'], secure=())

        mail_formatter = Formatter('''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s

            Message:

            %(message)s
            ''')

        file_formatter = Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        )

        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_formatter)
        app.logger.addHandler(mail_handler)

        file_handler = RotatingFileHandler(app.config['LOG_FILE'],
                                           maxBytes=10000000, backupCount=5)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.error("Application startup! Logging started for environment: %s" % app.config['ENVIRONMENT'])

        @app.errorhandler(429)
        def ratelimit_handler(e):
            app.logger.warning("Rate limit exceeded ({0})".format(e))
            return jsonify(error="ratelimit exceeded %s" % e.description), 429

        @app.errorhandler(Exception)
        def handle_error(e):
            code = 500
            if isinstance(e, HTTPException):
                code = e.code
            app.logger.error("Uncaught Exception ({0})".format(e))
            return jsonify(error=str(e)), code

        @app.before_request
        def pre_request_logging():
            app.logger.info("AUDIT log triggered. "
                            "time=({0}), "
                            "client_id=({1}), "
                            "client_ip=({2}), "
                            "request.method=({3}), "
                            "request.url=({4}), "
                            "request.data=({5}), "
                            "request.headers=({6})".format(
                datetime.datetime.today().ctime(),
                current_user.get_id(),
                get_client_ip(),
                request.method,
                request.url,
                request.data,
                ', '.join([': '.join(x) for x in request.headers])))
