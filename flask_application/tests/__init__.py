from flask_application import app
from flask_application.database.dataobject import ID_KEY
from flask_application.users.models import User
from flask_application.users.models import userdb
from flask_login import login_user
import json

TESTUSER1 = User(dict())
TESTUSER1_ID = '2455'
TESTUSER1.set_data(ID_KEY, TESTUSER1_ID)
TESTUSER1.set_data('name', 'testuser1')

@app.route('/auto_test_login')
def auto_login():
    userdb.set_user(TESTUSER1)
    login_user(TESTUSER1, remember=True)
    return "ok"
