from flask_application.database.dataobject import Dataobject
from flask_application.database.portaldb import db

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

ACTIVE_KEY = 'active'

def SourceGenerator(generator):
    for source in generator:
        yield Source(db.hgetall(source))

# source:userid:sourceid
class SourceDB():
    CLASSNAME = 'source'

    def set_source_for_user(self, userid, sourceobject):
        return db.hmset(self.CLASSNAME + ':' + userid + ':' + sourceobject.get_id(), sourceobject.as_dto())

    def get_source_for_user(self, userid, sourceid):
        return Source(db.hgetall(self.CLASSNAME + ':' + userid + ':' + sourceid))

    def del_source_from_user(self, userid, sourceid):
        return db.delete(self.CLASSNAME + ':' + userid + ':' + sourceid)

    def get_sources_for_user(self, userid):
        return SourceGenerator(db.scan_iter(match=self.CLASSNAME + ':' + userid + ':*'))

class Source(Dataobject):

    def set_values(self, values):
        self.merge_data_with_dict(values)

    def get_values(self):
        return self.as_dto()

# Create source database
sourcedb = SourceDB()
