# coding=utf-8
import unittest

from manage import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        # self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        # app.init_database()

    def tearDown(self):
        pass
        # os.unlink(app.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 200, rv.status_code
        assert '<!-- Header start -->' in rv.data
        assert '<!--导航 start -->' in rv.data
        assert '<!--main start-->' in rv.data
        assert '<!--版权 start-->' in rv.data
        assert 'utf-8', rv.charset
        return

if __name__ == '__main__':
    unittest.main()