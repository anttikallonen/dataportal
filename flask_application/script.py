from flask_script import Command
from flask_application.database.portaldb import db

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

class ResetDB(Command):
    def run(self, **kwargs):
        db.flushdb()
