from flask_application.source.models import sourcedb
from flask_application.tests.source import DatabaseTest
import logging
import json
from flask_application.tests.source import TESTUSER1_ID

class TestSourcedb(DatabaseTest):
    def test_source_db_should_store_one_source(self):
        sourcedb.set_source_for_user(TESTUSER1_ID, self.TESTSOURCE1)
        dbsource = list(sourcedb.get_sources_for_user(TESTUSER1_ID))[0]
        self.assertEquals(dbsource.get_id(), self.TESTSOURCE1_ID)
        self.assertEquals(dbsource.get_data('access_token'), 'token1')

    def test_source_db_should_be_able_to_update_source_values(self):
        sourcedb.set_source_for_user(TESTUSER1_ID, self.TESTSOURCE1)
        dbsource = list(sourcedb.get_sources_for_user(TESTUSER1_ID))[0]
        self.assertEquals(dbsource.get_id(), self.TESTSOURCE1_ID)
        self.assertEquals(dbsource.get_data('access_token'), 'token1')
        dbsource.set_values({'access_token': 'updated1', 'new_token': 'newtoken'})
        sourcedb.set_source_for_user(TESTUSER1_ID, dbsource)
        dbdbsourceupdated = sourcedb.get_source_for_user(TESTUSER1_ID, self.TESTSOURCE1_ID)
        self.assertEquals(dbdbsourceupdated.get_data('access_token'), 'updated1')
        self.assertEquals(dbdbsourceupdated.get_data('new_token'), 'newtoken')

    def test_source_db_should_store_multiple_sources_for_user(self):
        sourcedb.set_source_for_user(TESTUSER1_ID, self.TESTSOURCE1)
        sourcedb.set_source_for_user(TESTUSER1_ID, self.TESTSOURCE2)
        dbsources = list(sourcedb.get_sources_for_user(TESTUSER1_ID))
        self.assertEquals(len(dbsources), 2)

    def test_source_db_should_be_able_to_remove_one_source_from_user(self):
        sourcedb.set_source_for_user(TESTUSER1_ID, self.TESTSOURCE1)
        sourcedb.set_source_for_user(TESTUSER1_ID, self.TESTSOURCE2)
        dbsources = list(sourcedb.get_sources_for_user(TESTUSER1_ID))
        self.assertEquals(len(dbsources), 2)
        sourcedb.del_source_from_user(TESTUSER1_ID, dbsources[0].get_id())
        dbsources = list(sourcedb.get_sources_for_user(TESTUSER1_ID))
        self.assertEquals(len(dbsources), 1)