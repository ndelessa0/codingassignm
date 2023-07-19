import unittest
from app import app
from database import db
from models.user import UserModel

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        response = self.app.post('/register', json={'username': 'test_user', 'password': 'password'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'User created successfully.')


    def test_register_missing_username(self):
        response = self.app.post('/register', json={'password': 'password'})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['message'], {'username': 'This field cannot be left blank.'})

        
    def test_register_missing_password(self):
        response = self.app.post('/register', json={'username': 'test_user'})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['message'], {'password': 'This field cannot be left blank.'})


    def test_register_existing_username(self):
        response = self.app.post('/register', json={'username': 'test_user', 'password': 'password'})
        self.assertEqual(response.status_code, 201)

        # Attempt to register with the same username again
        response = self.app.post('/register', json={'username': 'test_user', 'password': 'password'})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['message'], 'A user with that username already exists.')

    def test_login(self):
        # Register a user
        response = self.app.post('/register', json={'username': 'test_user', 'password': 'password'})
        self.assertEqual(response.status_code, 201)

        # Attempt to login with correct credentials
        response = self.app.post('/login', json={'username': 'test_user', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('access_token', data)

    def test_login_incorrect_credentials(self):
        # Register a user
        response = self.app.post('/register', json={'username': 'test_user', 'password': 'password'})
        self.assertEqual(response.status_code, 201)

        # Attempt to login with incorrect password
        response = self.app.post('/login', json={'username': 'test_user', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['message'], 'Invalid credentials.')

if __name__ == '__main__':
    unittest.main()
