from flask_application.source.models import sourcedb
from flask_application.tests.source import DatabaseTest
from flask_application.tests import TESTUSER1_ID
import logging
import json

# Send data like this
# self.client.put('/api/keys/W2E_KEY',
# data=json.dumps(dict(VALUE="W2E_VALUE_UPDATED")),
# content_type="application/json")

class TestSourcerest(DatabaseTest):

    def test_get_current_user_source_link_active(self):
        sourcedb.set_source_for_user(TESTUSER1_ID, self.TESTSOURCE1)
        sourcedb.set_source_for_user(TESTUSER1_ID, self.TESTSOURCE2)
        with self.client:
            self.client.get('/auto_test_login')
            status = json.loads(self.client.get('/api/source/' + self.TESTSOURCE1_ID + '/active').data)
            self.assertEquals(status['active'], "true")
            status = json.loads(self.client.get('/api/source/' + self.TESTSOURCE2_ID + '/active').data)
            self.assertEquals(status['active'], "false")

    def test_get_current_user_source_link_active_nonexistent_source(self):
        sourcedb.set_source_for_user(TESTUSER1_ID, self.TESTSOURCE1)
        sourcedb.set_source_for_user(TESTUSER1_ID, self.TESTSOURCE2)
        with self.client:
            self.client.get('/auto_test_login')
            status = json.loads(self.client.get('/api/source/NONEXISTENT/active').data)
            self.assertEquals(status['active'], "false")
