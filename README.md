# Flask RESTful API with User Notes

This is a Flask RESTful API that allows users to manage their notes. Users can add, delete, and modify their notes, as well as filter notes by tags. The API requires users to be logged in to perform these actions. Notes can be marked as public or private, and public notes can be viewed by anyone without authentication.

## Features

- Users can add, delete, and modify their notes
- Users can see a list of all their notes
- Users can filter their notes via tags
- Users must be logged in to view, add, delete, and modify their notes
- Search contents of notes with keywords
- Notes can be either public or private
- Public notes can be viewed without authentication, but cannot be modified
- User management API to create new users

## API Endpoints

- POST /users - Create a new user
- POST /login - Login with username and password
- GET /notes - Get list of user's notes
- POST /notes - Create a new note
- GET /notes/<id> - Get a specific note
- PUT /notes/<id> - Update a note
- DELETE /notes/<id> - Delete a note
- GET /search/ - Search notes by keyword

## Technologies Used

- Flask: Python web framework for building the RESTful API
- Flask-RESTful: Extension for creating RESTful APIs with Flask
- Flask-JWT-Extended: Extension for JSON Web Token (JWT) authentication
- SQLAlchemy: Python SQL toolkit and Object-Relational Mapping (ORM) library
- SQLite: Simple database for storing user and note data


## Installation, Setup and Usage
The app can be run locally or via Docker.

## Local
Clone the repo
```
   git clone https://github.com/ndelessa0/codingassignm.git
   cd codingassignm
```
Create and activate a virtual environment(Optional but Recommended)

Install requirements
```
   pip install -r requirements.txt
```
Run the app: 
```
   python app.py
```  
The server will run at http://localhost:5000

## Docker
Clone the repo
```
   git clone https://github.com/ndelessa0/codingassignm.git
   cd codingassignm
```
Build the Docker image
```
   docker build -t <image-name> .
```
Run the Docker container
```
   docker run -p 5000:5000 <image-name>
```
The server will run at http://localhost:5000


## Tests
Tests are located in the /tests folder. To run tests:
   cd codingassignm
   pytest 
   
## File Structure
├── app.py                  # Main Flask app
├── config.py               # App config 
├── database.py             # Database setup and models
├── models
│   ├── note.py             # Note model
│   └── user.py             # User model
├── resources
│   ├── note.py             # Note API endpoints 
│   └── user.py             # User API endpoints
├── tests
│   ├── test_note.py        # Note tests
│   └── test_user.py        # User tests
├── requirements.txt
└── Dockerfile

