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

## Technologies Used

- Flask: Python web framework for building the RESTful API
- Flask-RESTful: Extension for creating RESTful APIs with Flask
- Flask-JWT-Extended: Extension for JSON Web Token (JWT) authentication
- SQLAlchemy: Python SQL toolkit and Object-Relational Mapping (ORM) library
- SQLite: Simple database for storing user and note data

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/ndelessa0/codingassignm.git
