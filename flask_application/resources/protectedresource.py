from flask_restful import Resource
from flask_login import login_required

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

class ProtectedResource(Resource):
    method_decorators = [login_required]
