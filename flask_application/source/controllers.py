import os
from flask import Blueprint, request
from flask_login import login_required, current_user, current_app
import flask_restful as restful
from flask_application.resources.protectedresource import ProtectedResource
from flask_login import current_user
from flask import jsonify
from flask_application.source.models import sourcedb, Source, ACTIVE_KEY
from flask import current_app
import json

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

source = Blueprint('source', __name__)
api = restful.Api(source, prefix="/api")

class SourceStatusAPI(ProtectedResource):

    def get(self, id):
        current_app.logger.info("User ({0}) requested source active status with id ({1})".format(current_user.get_id(), id))
        target_source = sourcedb.get_source_for_user(current_user.get_id(), id)
        if target_source.as_dto():
            return {'active': target_source.get_data(ACTIVE_KEY)}
        return {'active': 'false'}

api.add_resource(SourceStatusAPI, '/source/<string:id>/active')
