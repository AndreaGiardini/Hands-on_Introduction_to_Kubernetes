import os
import unittest

from app import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        pass

    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_liveness_page(self):
        response = self.app.get('/liveness', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/liveness/change', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/liveness', follow_redirects=True)
        self.assertEqual(response.status_code, 500)
        response = self.app.get('/liveness/change', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/liveness', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_readiness_page(self):
        response = self.app.get('/readiness', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/readiness/change', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/readiness', follow_redirects=True)
        self.assertEqual(response.status_code, 500)
        response = self.app.get('/readiness/change', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/readiness', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_prime_page(self):
        response = self.app.get('/prime', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/prime/100', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

class EnvTests(unittest.TestCase):

    def setUp(self):
        os.environ['COLOR'] = "green"
        self.app = app.test_client()
        pass

    def tearDown(self):
        del os.environ['COLOR']
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('green'.encode(), response.data)

class LoginTests(unittest.TestCase):

    def setUp(self):
        os.environ['LOGIN_USER'] = "admin"
        os.environ['LOGIN_PASS'] = "1234"
        self.app = app.test_client()
        pass

    def tearDown(self):
        del os.environ['LOGIN_USER']
        del os.environ['LOGIN_PASS']
        pass

    def test_main_page(self):
        response = self.app.post('/login', data={'username': 'admin', 'password': '1234'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successful'.encode(), response.data)
        response = self.app.post('/login', data={'username': 'nouser', 'password': 'nopass'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Failed'.encode(), response.data)

if __name__ == "__main__":
    unittest.main()
