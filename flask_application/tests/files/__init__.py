from flask import current_app
from flask_testing import TestCase
from flask_application import app
from flask_application.script import ResetDB
from flask_application.database.dataobject import ID_KEY
from flask_application.files.models import File
from flask_application.users.models import User
from flask_application.users.models import userdb
from flask_login import login_user
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
        self.client = self.app.test_client()

        self.TESTFILE1 = File(dict())
        self.TESTFILE1_ID = '1234'
        self.TESTFILE1.set_data(ID_KEY, self.TESTFILE1_ID)
        self.TESTFILE1.set_data('filename', 'testfile1.csv')

        self.TESTFILE2 = File(dict())
        self.TESTFILE2_ID = '1236'
        self.TESTFILE2.set_data(ID_KEY, self.TESTFILE2_ID)
        self.TESTFILE2.set_data('filename', 'testfile2.csv')

    def tearDown(self):
        ResetDB().run()
