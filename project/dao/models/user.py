from marshmallow import Schema, fields

from project.setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    favorite_genre = db.Column(db.Integer, db.ForeignKey("genre.id"))
    email = db.Column(db.String)


class UserSchema(Schema):
    id = fields.Int()
    role = fields.Str()
    username = fields.Str()
    password = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Int()
    email = fields.Str()
