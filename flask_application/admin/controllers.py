import os
from flask import Blueprint, request, send_file
from flask_login import login_required, current_user, current_app
import flask_restful as restful
from flask_login import current_user
from flask_restful import Resource
from flask_application.users.models import userdb
from flask_application.files.models import filedb
from flask_application.source.models import sourcedb
from flask_application.files.controllers import resolve_file_path
from flask import current_app
from flask_application.utils.client import *
from flask_application import app
from functools import wraps
from flask import abort
import jwt

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"


# removed HMAC handling

admin = Blueprint('admin', __name__)
api = restful.Api(admin, prefix="/api")


class UserListAPI(Resource):
    method_decorators = [admin_required]

    def get(self):
        return map(lambda x: x.get_id(), userdb.get_all_users())


class UserInfoAPI(Resource):
    method_decorators = [admin_required]

    def get(self, id):
        userobject = userdb.get_user(id)
        if userobject:
            return userobject.as_dto()
        else:
            return {}, 404


class FileListAPI(Resource):
    method_decorators = [admin_required]

    def get(self, id):
        return map(lambda x: x.as_dto(), filedb.get_files_for_user(id))

class FileDownloadAPI(Resource):
    method_decorators = [admin_required]

    def get(self, id):
        return send_file(resolve_file_path(id))


class SourceListAPI(Resource):
    method_decorators = [admin_required]

    def get(self, id):
        return map(lambda x: x.as_dto(), sourcedb.get_sources_for_user(id))

api.add_resource(UserListAPI, '/admin/users')
api.add_resource(UserInfoAPI, '/admin/user/<string:id>/userinfo')
api.add_resource(FileListAPI, '/admin/user/<string:id>/files')
api.add_resource(FileDownloadAPI, '/admin/file/<string:id>/download')
api.add_resource(SourceListAPI, '/admin/user/<string:id>/sources')
