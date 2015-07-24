import unittest
import tempfile

import os
import app


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        # self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        # app.init_database()

    def tearDown(self):
        pass
        # os.unlink(app.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Hello World' in rv.data
        return

if __name__ == '__main__':
    unittest.main()