import os
from flask import Blueprint, request
from flask_login import login_required, current_user, current_app
from werkzeug.utils import secure_filename
import flask_restful as restful
from flask_application.resources.protectedresource import ProtectedResource
from flask_login import current_user
from flask import jsonify
from flask_application.database.dataobject import ID_KEY
from flask_application.files.models import filedb, File, \
    FILEOBJECT_FILENAME_KEY, FILEOBJECT_TIMESTAMP_KEY
import json
import uuid
import arrow
from flask import current_app

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"


files = Blueprint('files', __name__)
api = restful.Api(files, prefix="/api")


def resolve_file_path(fileid):
    return os.path.join(current_app.config['UPLOAD_FOLDER'],
                        fileid + '.dat')

class FileListAPI(ProtectedResource):
    def get(self):
        current_app.logger.info("User ({0}) requested file listing".format(current_user.get_id()))
        return [f.as_dto() for f in filedb.get_files_for_user(current_user.get_id())]

    def post(self):
        file = request.files['file']
        fileobject = File(dict())
        filename = secure_filename(file.filename)
        fileobject.set_id(str(uuid.uuid4()))
        fileobject.set_data(FILEOBJECT_TIMESTAMP_KEY, str(arrow.now().timestamp))
        fileobject.set_data(FILEOBJECT_FILENAME_KEY, filename)
        try:
            file.save(resolve_file_path(fileobject.get_id()))
        except Exception as e:
            current_app.logger.error("Failed to save file to filesystem ({0})".format(e))
        filedb.set_file_for_user(current_user.get_id(), fileobject)
        current_app.logger.info("User ({0}) uploaded file ({1})".format(current_user.get_id(), filename.encode('utf-8').strip()))


    def delete(self):
        fileid = request.args.get(ID_KEY)
        fileobject = filedb.get_file_for_user(current_user.get_id(), fileid)
        try:
            os.remove(resolve_file_path(fileobject.get_id()))
        except Exception as e:
            current_app.logger.error("Failed to remove file from filesystem ({0})".format(e))
        filedb.del_file_from_user(current_user.get_id(), fileobject)
        current_app.logger.info("User ({0}) deleted file ({1})".format(current_user.get_id(), fileobject.get_data(FILEOBJECT_FILENAME_KEY)))


api.add_resource(FileListAPI, '/files')
