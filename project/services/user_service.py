import base64
import hashlib

from flask import current_app
from sqlalchemy.orm import scoped_session

from coursework_3_source.project.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from coursework_3_source.project.dao.models.user import UserSchema
from coursework_3_source.project.dao.user import UserDAO
from coursework_3_source.project.exceptions import ItemNotFound
from coursework_3_source.project.services.base import BaseService
from coursework_3_source.project.tools.security import generate_password_digest


class UserService(BaseService):
    def __init__(self, session: scoped_session):
        super().__init__(session)
        self.dao = None

    def get_item_by_id(self, pk):
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_item_by_email(self, email):
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def get_limit_users(self):
        limit = current_app.config["ITEMS_PER_PAGE"]
        offset = ("page" - 1) * limit
        users = UserDAO(self._db_session).get_limit(limit=limit, offset=offset)
        return UserSchema(many=True).dump(users)

    def create(self, data_in):
        user_pass = data_in.get("password")
        if user_pass:
            data_in["password"] = generate_password_digest(user_pass)
        user = UserDAO(self._db_session).create(data_in)
        return UserSchema().dump(user)

    def update(self, data_in):
        user = UserDAO(self._db_session).update(data_in)
        return UserSchema().dump(user)

    def update_pass(self, data_in):
        user_pass_1 = data_in.get("password_1")
        user_pass_2 = data_in.get("password_2")
        # user_pass_1 = UserDAO(self._db_session).update(data_in)
        # return UserSchema().dump(user)


def get_hash(password):
    return base64.b64encode(hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                                PWD_HASH_SALT,
                                                PWD_HASH_ITERATIONS
                                                ))
