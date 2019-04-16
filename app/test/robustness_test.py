
import unittest
from app import app
from app.forms import LoginForm
import uuid


class FlaskTestCase(unittest.TestCase):

    # Brute force test to ensure throttling works
    def test_brute_force(self):
        tester = app.test_client()
        for i in range(100):
            tester.post(
                '/login',
                data=dict(username="wrong", password="alsowrong"),
                follow_redirects=True
            )
        response = tester.post(
            '/login',
            data=dict(username="wrong", password="alsowrong"),
            follow_redirects=True
        )
        self.assertIn(b'Too Many Requests', response.data)

    def test_login_injection(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username=" ' OR true--", password="Password1"),
            follow_redirects=True
        )
        self.assertIn(b'<title>Login Page</title>', response.data)

    def test_register_injection(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username=" ' OR true--", password="Password1"),
            follow_redirects=True
        )
        self.assertIn(b'<title>Login Page</title>', response.data)

    def test_empty_register1(self):
        tester = app.test_client()
        response = tester.post(
            '/register',
            data=dict(email="something@example.com", username="something'; DROP TABLE users;",
                      password="admin", password2="admin"),
            follow_redirects=True
        )
        self.assertIn(b'[This field is required.]', response.data)

if __name__ == '__main__':
    unittest.main()