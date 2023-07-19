from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import Config
from resources.user import UserRegister, UserLogin
from resources.note import Note, NoteList, NoteSearch
from database import db
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager()
api = Api(app)
jwt.init_app(app)

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Note, '/note/<int:note_id>','/note')
api.add_resource(NoteList, '/notes')
api.add_resource(NoteSearch,'/search/')

with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
