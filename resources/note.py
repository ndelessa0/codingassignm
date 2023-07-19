from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.note import NoteModel
import logging
from flask import jsonify

logger = logging.getLogger(__name__)


class Note(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help='This field cannot be left blank.')
    parser.add_argument('body', type=str, required=True, help='This field cannot be left blank.')
    parser.add_argument('tags', type=str)
    parser.add_argument('public', type=bool, default=False)

    @jwt_required()
    def get(self, note_id):
        note = NoteModel.find_by_id(note_id)

        if note:
            if note.public:
                return note.serialize(), 200
            else:
                user_id = get_jwt_identity()
                if note.user_id == user_id:
                    return note.serialize(), 200
                return {'message': 'Access denied.'}, 401

        return {'message': 'Note not found.'}, 404

    @jwt_required()
    def post(self):

        data = Note.parser.parse_args()
        user_id = get_jwt_identity()

        note = NoteModel(title=data['title'], body=data['body'], tags=data['tags'], public=data['public'], user_id=user_id)

        try:
            note.save_to_db()
        except:
            return {'message': 'An error occurred while creating the note.'}, 500
        return note.serialize(), 201



    @jwt_required()
    def put(self, note_id):
        data = Note.parser.parse_args()
        note = NoteModel.find_by_id(note_id)

        if note:
            user_id = get_jwt_identity()
            if note.user_id == user_id:
                note.title = data['title']
                note.body = data['body']
                note.tags = data['tags']
                note.public = data['public']
                note.save_to_db()
                return note.serialize(), 200
            return {'message': 'Access denied.'}, 401

        return {'message': 'Note not found.'}, 404

    @jwt_required()
    def delete(self, note_id):
        note = NoteModel.find_by_id(note_id)

        if note:
            user_id = get_jwt_identity()
            if note.user_id == user_id:
                note.delete_from_db()
                return {'message': 'Note deleted.'}, 200
            return {'message': 'Access denied.'}, 401

        return {'message': 'Note not found.'}, 404

class NoteList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        notes = NoteModel.query.filter_by(user_id=user_id).all()
        print(len(notes))
        return {'notes': [note.serialize() for note in notes]}, 200
    
class NoteSearch(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, location='args', required=True, help='This field cannot be left blank.')
        args = parser.parse_args()

        search_query = args['q']
        search_results = NoteModel.search_notes(search_query)
        return [note.serialize() for note in search_results], 200
    

