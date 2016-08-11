from flask_application.files.models import filedb
from flask_application.tests.files import DatabaseTest
from flask_application.database.dataobject import ID_KEY
from flask_application.tests import TESTUSER1_ID
import logging
import json


class TestFilerest(DatabaseTest):

    def test_get_current_user_files(self):
        filedb.set_file_for_user(TESTUSER1_ID, self.TESTFILE1)
        filedb.set_file_for_user(TESTUSER1_ID, self.TESTFILE2)
        with self.client:
            self.client.get('/auto_test_login')
            jsondata = json.loads(self.client.get('/api/files').data)
            self.assertEquals(len(jsondata), 2)

    def test_delete_current_user_file(self):
        filedb.set_file_for_user(TESTUSER1_ID, self.TESTFILE1)
        filedb.set_file_for_user(TESTUSER1_ID, self.TESTFILE2)
        with self.client:
            self.client.get('/auto_test_login')
            self.client.delete('/api/files?id=' + self.TESTFILE1.get_id())
            jsondata = json.loads(self.client.get('/api/files').data)
            self.assertEquals(len(jsondata), 1)