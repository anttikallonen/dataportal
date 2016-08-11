import json
import copy

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

ID_KEY = "id"

class Dataobject():
    objectdata = dict()

    def __init__(self, objectdto):
        self.objectdata = objectdto

    def set_id(self, id):
        self.objectdata[ID_KEY] = id

    def get_id(self):
        return str(self.objectdata[ID_KEY])

    def as_dto(self):
        return self.objectdata

    def get_data(self, key):
        if not key in self.objectdata:
            return None
        return self.objectdata[key]

    def set_data(self, key, data):
        self.objectdata[key] = data

    def merge_data_with_dict(self, newdata):
        for key, val in newdata.items():
            self.objectdata[key] = val

    def __str__(self):
        return json.dumps(self.objectdata)

    def __repr__(self):
        return json.dumps(self.objectdata)
