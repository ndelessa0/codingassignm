import unittest
import string
import random
from app import app, db
from models.note import NoteModel

def generate_random_string(length):
    """Generate a random string of alphanumeric characters."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

class NoteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def register_and_login(self):
        # Generate random username and password
        username = generate_random_string(10)
        password = generate_random_string(10)

        # Register the test user
        response = self.app.post('/register', json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 201)

        # Login as the test user
        response = self.app.post('/login', json={'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)

        # Get the access token
        data = response.get_json()
        access_token = data['access_token']
        
        return access_token

    def test_add_note(self):
        access_token = self.register_and_login()
        headers ={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
        }
        # Test adding a note
        data = {
            'title': 'Test Note 1',
            'body': 'Note content 1',
            'tags': 'Tag1, Tag2',
            'public': True
        }
        response = self.app.post('/note', headers=headers, json=data)
        self.assertEqual(response.status_code, 201)

        # Test adding a note without authentication
        response = self.app.post('/note', json=data)
        self.assertEqual(response.status_code, 500)

        # Add more assertions as needed

    def test_get_note(self):
        access_token = self.register_and_login()

        # Add a new note for the test user
        data = {
            'title': 'Test Note',
            'body': 'Note content',
            'tags': 'Tag1, Tag2',
            'public': True
        }
        headers ={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
        }
        response = self.app.post('/note', headers=headers, json=data)
        self.assertEqual(response.status_code, 201)
        note_id = response.get_json()['id']

        # Test getting the note
        response = self.app.get(f'/note/{note_id}', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], 'Test Note')

        # Test getting notes without authentication
        response = self.app.get('/note')
        self.assertEqual(response.status_code, 500)

        # Add more assertions as needed
    
    def test_update_note(self):
        access_token = self.register_and_login()
        headers ={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
        }
        # Add a new note for the test user
        data = {
            'title': 'Test Note',
            'body': 'Note content',
            'tags': 'Tag1, Tag2',
            'public': True
        }
        response = self.app.post('/note', headers=headers, json=data)
        self.assertEqual(response.status_code, 201)
        note_id = response.get_json()['id']

        # Test updating the note
        updated_data = {
            'title': 'Updated Note',
            'body': 'Updated content',
            'tags': 'Tag3, Tag4',
            'public': False
        }
        response = self.app.put(f'/note/{note_id}', headers=headers, json=updated_data)
        self.assertEqual(response.status_code, 200)

        # Test updating a non-existent note
        response = self.app.put('/note/999', headers=headers, json=updated_data)
        self.assertEqual(response.status_code, 404)

        # Test updating a note without authentication
        response = self.app.put(f'/note/{note_id}', json=updated_data)
        self.assertEqual(response.status_code, 500)

        # Add more assertions as needed
    
    def test_delete_note(self):
        access_token = self.register_and_login()
        headers ={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
        }
        # Add a new note for the test user
        data = {
            'title': 'Test Note',
            'body': 'Note content',
            'tags': 'Tag1, Tag2',
            'public': True
        }
        response = self.app.post('/note', headers=headers, json=data)
        self.assertEqual(response.status_code, 201)
        note_id = response.get_json()['id']

        # Test deleting the note
        response = self.app.delete(f'/note/{note_id}', headers=headers)
        self.assertEqual(response.status_code, 200)

        # Test deleting a non-existent note
        response = self.app.delete('/note/999', headers=headers)
        self.assertEqual(response.status_code, 404)

        # Test deleting a note without authentication
        response = self.app.delete(f'/note/{note_id}')
        self.assertEqual(response.status_code, 500)

        # Add more assertions as needed

    def test_get_all_notes(self):
        access_token = self.register_and_login()
        headers ={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
        }
        # Add multiple notes for the test user
        data1 = {
            'title': 'Note 1',
            'body': 'Note content 1',
            'tags': 'Tag1, Tag2',
            'public': True
        }
        data2 = {
            'title': 'Note 2',
            'body': 'Note content 2',
            'tags': 'Tag3, Tag4',
            'public': False
        }
        self.app.post('/note', headers=headers, json=data1)
        self.app.post('/note', headers=headers, json=data2)

        # Test getting all notes
        response = self.app.get('/notes', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        print(data)
        self.assertEqual(len(data["notes"]), 2)

        # Add more assertions as needed

    def test_search_notes(self):
        access_token = self.register_and_login()
        headers ={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
        }
        # Add multiple notes for the test user
        data1 = {
            'title': 'Note 1',
            'body': 'Note content 1',
            'tags': 'Tag1, Tag2',
            'public': True
        }
        data2 = {
            'title': 'Note 2',
            'body': 'Note content 2',
            'tags': 'Tag3, Tag4',
            'public': False
        }
        self.app.post('/note', headers=headers, json=data1)
        self.app.post('/note', headers=headers, json=data2)

        # Test searching notes with keywords
        response = self.app.get('/search?q=content', headers={'Authorization': f'Bearer {access_token}'},follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)

        # Test searching notes with non-existent keyword
        response = self.app.get('/search?q=keyword', headers={'Authorization': f'Bearer {access_token}'},follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 0)

        # Add more assertions as needed
    
if __name__ == '__main__':
    unittest.main()
