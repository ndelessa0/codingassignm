from database import db

class NoteModel(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200))
    public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def serialize(note):
      return {
        'id': note.id,
        'title': note.title,
        'body': note.body,
        'tags': note.tags,
        'public': note.public 
      }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, note_id):
        return cls.query.filter_by(id=note_id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_user_id_and_tag(cls, user_id, tag):
        return cls.query.filter_by(user_id=user_id, tags=tag).all()

    @staticmethod
    def search_notes(keyword):
        return NoteModel.query.filter(
            db.or_(
                NoteModel.title.ilike(f'%{keyword}%'),
                NoteModel.body.ilike(f'%{keyword}%'),
                NoteModel.tags.ilike(f'%{keyword}%')
            )
        ).all()

