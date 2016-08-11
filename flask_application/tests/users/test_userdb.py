from flask_application.users.models import userdb
from flask_application.tests.users import DatabaseTest
from flask_application.database.dataobject import ID_KEY
import logging
import json

class TestUserdb(DatabaseTest):


    def test_user_db_should_store_one_user(self):
        userdb.set_user(self.TESTUSER1)
        dbuser = userdb.get_user(self.TESTUSER1_ID)
        self.assertEquals(dbuser.get_id(), self.TESTUSER1_ID)
        self.assertEquals(dbuser.get_data('name'), 'testuser1')

    def test_user_db_should_store_multiple_users(self):
        userdb.set_user(self.TESTUSER1)
        userdb.set_user(self.TESTUSER2)
        dbuser1 = userdb.get_user(self.TESTUSER1_ID)
        dbuser2 = userdb.get_user(self.TESTUSER2_ID)
        self.assertEquals(dbuser1.get_id(), self.TESTUSER1_ID)
        self.assertEquals(dbuser1.get_data('name'), 'testuser1')
        self.assertEquals(dbuser1.get_data('name'), 'testuser1')
        self.assertEquals(dbuser2.get_id(), self.TESTUSER2_ID)
        self.assertEquals(dbuser2.get_data('name'), 'testuser2')
        users = list(userdb.get_all_users())
        self.assertEquals(len(users), 2)

    def test_user_db_should_be_able_to_update_user(self):
        userdb.set_user(self.TESTUSER1)
        userdb.set_user(self.TESTUSER2)
        dbuser1 = userdb.get_user(self.TESTUSER1_ID)
        dbuser2 = userdb.get_user(self.TESTUSER2_ID)
        self.assertEquals(dbuser1.get_id(), self.TESTUSER1_ID)
        self.assertEquals(dbuser1.get_data('name'), 'testuser1')
        self.assertEquals(dbuser2.get_id(), self.TESTUSER2_ID)
        self.assertEquals(dbuser2.get_data('name'), 'testuser2')
        users = list(userdb.get_all_users())
        self.assertEquals(len(users), 2)
        # Update data
        self.TESTUSER1.set_data('name', 'testuser1updated')
        userdb.set_user(self.TESTUSER1)
        # Check that data updated correctly
        dbuser1 = userdb.get_user(self.TESTUSER1_ID)
        dbuser2 = userdb.get_user(self.TESTUSER2_ID)
        self.assertEquals(dbuser1.get_id(), self.TESTUSER1_ID)
        self.assertEquals(dbuser1.get_data('name'), 'testuser1updated')
        self.assertEquals(dbuser2.get_id(), self.TESTUSER2_ID)
        self.assertEquals(dbuser2.get_data('name'), 'testuser2')
        users = list(userdb.get_all_users())
        self.assertEquals(len(users), 2)

    def test_user_db_should_be_able_to_remove_only_one_user(self):
        userdb.set_user(self.TESTUSER1)
        userdb.set_user(self.TESTUSER2)
        dbuser1 = userdb.get_user(self.TESTUSER1_ID)
        dbuser2 = userdb.get_user(self.TESTUSER2_ID)
        self.assertEquals(dbuser1.get_id(), self.TESTUSER1_ID)
        self.assertEquals(dbuser1.get_data('name'), 'testuser1')
        self.assertEquals(dbuser2.get_id(), self.TESTUSER2_ID)
        self.assertEquals(dbuser2.get_data('name'), 'testuser2')
        users = list(userdb.get_all_users())
        self.assertEquals(len(users), 2)
        # Remove user
        userdb.del_user(self.TESTUSER1)
        # Check that data removed correctly
        dbuser1 = userdb.get_user(self.TESTUSER1_ID)
        dbuser2 = userdb.get_user(self.TESTUSER2_ID)
        self.assertIsNone(dbuser1)
        self.assertEquals(dbuser2.get_id(), self.TESTUSER2_ID)
        self.assertEquals(dbuser2.get_data('name'), 'testuser2')
        users = list(userdb.get_all_users())
        self.assertEquals(len(users), 1)
