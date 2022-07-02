from flask import current_app
from sqlalchemy.orm import scoped_session


from project.dao.models.user import UserSchema
from project.dao.user import UserDAO
from project.exceptions import ItemNotFound
from project.services.base import BaseService
from project.tools.security import generate_password_hash, compare_passwords


class UserService(BaseService):
    def __init__(self, session: scoped_session):
        super().__init__(session)
        self.dao = None

    def get_item_by_id(self, pk):
        """
        Получение пользователя по id
        :param pk: id пользователя
        :return: данные пользователя в формате json
        """
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_item_by_email(self, email):
        """
        Получение пользователя по email
        :param email: email пользователя
        :return: данные пользователя в формате json
        """
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def create(self, data_in):
        """
        Создает нового пользователя
        :param data_in: полученные данные для нового пользователя
        :return: нового пользователя
        """
        user_pass = data_in.get("password")
        if user_pass:
            data_in["password"] = generate_password_hash(user_pass)
        user = UserDAO(self._db_session).create(data_in)
        return UserSchema().dump(user)

    def update(self, data_in):
        """
        Изменение пользователя
        :param data_in: данные которые необходимо изменить
        :return: Новые данные пользователя, с учетом изменений
        """
        user = UserDAO(self._db_session).update(data_in)
        return UserSchema().dump(user)

    def update_pass(self, data_in):
        """
        Изменение пароля
        :return: Новые данные пользователя, с учетом изменений
        """
        user_pass_1 = data_in.get("password_1")
        user_pass_2 = data_in.get("password_2")
        user = UserDAO(self._db_session).get_by_id(data_in)
        if compare_passwords(user.password, user_pass_1):
            user.password = generate_password_hash(user_pass_2)
            update_user = UserDAO(self._db_session).update(user)
            return UserSchema().dump(update_user)
        return None
