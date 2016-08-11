from flask import current_app
from flask_testing import TestCase
from flask_application import app
from flask_application.script import ResetDB
from flask_application.database.dataobject import ID_KEY
from flask_application.users.models import User
import json


class DatabaseTest(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        self.assertTrue(
            current_app.config['TESTING'],
            'Testing is not set. Are you sure you are using the right config?'
        )
        ResetDB().run()

        self.TESTUSER1 = User(dict())
        self.TESTUSER1_ID = '1234'
        self.TESTUSER1.set_data(ID_KEY, self.TESTUSER1_ID)
        self.TESTUSER1.set_data('name', 'testuser1')

        self.TESTUSER2 = User(dict())
        self.TESTUSER2_ID = '1236'
        self.TESTUSER2.set_data(ID_KEY, self.TESTUSER2_ID)
        self.TESTUSER2.set_data('name', 'testuser2')

    def tearDown(self):
        ResetDB().run()