from mongoengine import Document, fields

class Note(Document):
    title = fields.StringField(max_length=255, required=True)
    description = fields.StringField(required=True)
    audio = fields.FileField(upload_to='notes/audio/')
    pdf = fields.FileField(upload_to='notes/pdf/')

class Quiz(Document):
    prompt = fields.StringField(required=True)
    pdf = fields.FileField(upload_to='quizzes/pdf/')

class NoteWithBinaryFile(Document):
    title = fields.StringField(max_length=255, required=True)
    description = fields.StringField(required=True)
    audio = fields.FileField(upload_to='notes/audio/')
    pdf = fields.FileField(upload_to='notes/pdf/')