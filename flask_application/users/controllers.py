from flask import Blueprint
import flask_restful as restful
from flask_application.resources.protectedresource import ProtectedResource
from flask_login import current_user
from flask import redirect, url_for, current_app
from flask_login import logout_user
from flask import jsonify
import logging

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"


class CurrentUserResource(ProtectedResource):
    def get(self):
        current_app.logger.info("Getting user info for user ({0})".format(
            current_user))
        return jsonify(current_user.as_dto())


users = Blueprint('users', __name__)
api = restful.Api(users, prefix="/api")
api.add_resource(CurrentUserResource, "/user")
