from flask import current_app
from flask_testing import TestCase
from flask_application import app
from flask_application.script import ResetDB
from flask_application.database.dataobject import ID_KEY
from flask_application.source.models import Source
from flask_application.users.models import User
from flask_application.users.models import userdb
from flask_login import login_user
import json

TESTUSER1 = User(dict())
TESTUSER1_ID = '2455'
TESTUSER1.set_data(ID_KEY, TESTUSER1_ID)
TESTUSER1.set_data('name', 'testuser1')

class DatabaseTest(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        self.assertTrue(
            current_app.config['TESTING'],
            'Testing is not set. Are you sure you are using the right config?'
        )
        ResetDB().run()
        self.client = self.app.test_client()

        tokens1 = {'access_token': 'token1', 'active': 'true'}
        self.TESTSOURCE1 = Source(dict())
        self.TESTSOURCE1_ID = 'W2E_SOURCE1'
        self.TESTSOURCE1.set_id(self.TESTSOURCE1_ID)
        self.TESTSOURCE1.set_values(tokens1)

        tokens2 = {'access_token': 'token2', 'active': 'false'}
        self.TESTSOURCE2 = Source(dict())
        self.TESTSOURCE2_ID = 'W2E_SOURCE2'
        self.TESTSOURCE2.set_id(self.TESTSOURCE2_ID)
        self.TESTSOURCE2.set_values(tokens2)

    def tearDown(self):
        ResetDB().run()

