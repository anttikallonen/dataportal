__author__ = 'antti'
from flask_application.database.dataobject import Dataobject
from flask_application.database.portaldb import db

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

FILEOBJECT_FILENAME_KEY = "filename"
FILEOBJECT_TIMESTAMP_KEY = "timestamp_unixtime"

def FileGenerator(generator):
    for key in generator:
        yield File(db.hgetall(key))

# file:userid:fileid
class FileDB():
    CLASSNAME = 'file'

    def set_file_for_user(self, userid, fileobject):
        return db.hmset(self.CLASSNAME + ':' + userid + ':' + fileobject.get_id(), fileobject.as_dto())

    def get_file_for_user(self, userid, fileid):
        return File(db.hgetall(self.CLASSNAME + ':' + userid + ':' + fileid))

    def del_file_from_user(self, userid, fileobject):
        return db.delete(self.CLASSNAME + ':' + userid + ':' + fileobject.get_id())

    def get_files_for_user(self, userid):
        return FileGenerator(db.scan_iter(match=self.CLASSNAME + ':' + userid + ':*'))

class File(Dataobject):
    pass

# Create file database
filedb = FileDB()




