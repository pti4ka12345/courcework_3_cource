from marshmallow import Schema, fields

from coursework_3_source.project.dao.models.base import BaseMixin
from coursework_3_source.project.setup_db import db


class Director(BaseMixin, db.Model):
    __tablename__ = 'director'
    name = db.Column(db.String(255))

    def __repr__(self):
        return f"<Director '{self.name.title()}'>"

class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
