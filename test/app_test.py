# coding=utf-8
import unittest

from start import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        # self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        # app.init_database()

    def tearDown(self):
        pass
        # os.unlink(app.app.config['DATABASE'])

    def test_index_page(self):
        rv = self.app.get('/')
        assert 200, rv.status_code
        assert '<!-- Header start -->' in rv.data
        assert '<!--导航 start -->' in rv.data
        assert '<!--main start-->' in rv.data
        assert '<!--版权 start-->' in rv.data
        assert 'utf-8', rv.charset

    def test_admin_index_page(self):
        rv = self.app.get('/admin')
        assert 200, rv.status_code
        assert '<a href="/admin/user/">', rv.data
        assert '<a href="/admin/role/">', rv.data
        assert '<a href="/admin/enumvalues/">', rv.data
        assert 'utf-8', rv.charset

if __name__ == '__main__':
    unittest.main()
