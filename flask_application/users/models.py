from flask_application.database.dataobject import Dataobject
from flask_application.database.portaldb import db
from flask_application.resources.protectedresource import ProtectedResource
from flask_login import current_user
from flask_application import login_manager
from flask import jsonify
import json

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

GOOGLE_NAME_KEY = "googlename"
GOOGLE_EMAIL_KEY = "googleemail"
W2E_ID_KEY = "w2eid"
W2E_ACCESS_TOKEN_KEY = "w2eaccesstoken"
W2E_REFRESH_TOKEN_KEY = "w2erefreshtoken"

def UserGenerator(generator):
    for key in generator:
        yield User(db.hgetall(key))

class UserDB():
    CLASSNAME = 'user'
    def set_user(self, userobject):
        id = userobject.get_id()
        dto = userobject.as_dto()
        return db.hmset(self.CLASSNAME + ':' + id, dto)

    def get_user(self, id):
        dto = db.hgetall(self.CLASSNAME + ':' + id)
        if dto:
            return User(dto)
        else:
            return None

    def get_all_users(self):
        return UserGenerator(db.scan_iter(match=self.CLASSNAME + '*'))

    def del_user(self, user):
        return db.delete(self.CLASSNAME + ':' + user.get_id())

class User(Dataobject):

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

# Create user database
userdb = UserDB()

@login_manager.user_loader
def load_user(id):
    return userdb.get_user(id)

def update_user(user):
    userdb.set_user(user)
