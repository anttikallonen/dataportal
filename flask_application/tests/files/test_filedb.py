from flask_application.files.models import filedb
from flask_application.tests.files import DatabaseTest
from flask_application.database.dataobject import ID_KEY
import logging
import json
from flask_application.tests import TESTUSER1_ID

class TestFiledb(DatabaseTest):
    def test_file_db_should_store_one_file(self):
        filedb.set_file_for_user(TESTUSER1_ID, self.TESTFILE1)
        dbfile = list(filedb.get_files_for_user(TESTUSER1_ID))[0]
        self.assertEquals(dbfile.get_id(), self.TESTFILE1_ID)
        self.assertEquals(dbfile.get_data('filename'), 'testfile1.csv')

    def test_file_db_should_store_multiple_files_for_user(self):
        filedb.set_file_for_user(TESTUSER1_ID, self.TESTFILE1)
        filedb.set_file_for_user(TESTUSER1_ID, self.TESTFILE2)
        dbfiles = list(filedb.get_files_for_user(TESTUSER1_ID))
        self.assertEquals(len(dbfiles), 2)

    def test_file_db_should_be_able_to_remove_one_file_from_user(self):
        filedb.set_file_for_user(TESTUSER1_ID, self.TESTFILE1)
        filedb.set_file_for_user(TESTUSER1_ID, self.TESTFILE2)
        dbfiles = list(filedb.get_files_for_user(TESTUSER1_ID))
        self.assertEquals(len(dbfiles), 2)
        filedb.del_file_from_user(TESTUSER1_ID, dbfiles[0])
        dbfiles = list(filedb.get_files_for_user(TESTUSER1_ID))
        self.assertEquals(len(dbfiles), 1)

