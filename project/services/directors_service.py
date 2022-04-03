from project.dao.director import DirectorDAO
from project.dao.models.director import DirectorSchema
from project.exceptions import ItemNotFound
from project.services.base import BaseService


class DirectorsService(BaseService):
    def get_item_by_id(self, pk):
        """
        Получение режисера по id
        :param pk: id режисера
        :return: данные о режисере в формате json
        """
        director = DirectorDAO(self._db_session).get_by_id(pk)
        if not director:
            raise ItemNotFound
        return DirectorSchema().dump(director)

    def get_all_directors(self):
        """
        Получение всех режисеров
        :return: все режисеры в json формате
        """
        directors = DirectorDAO(self._db_session).get_all()
        return DirectorSchema(many=True).dump(directors)