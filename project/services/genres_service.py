from project.dao.genre import GenreDAO
from project.dao.models.genre import GenreSchema
from project.exceptions import ItemNotFound
from project.services.base import BaseService


class GenresService(BaseService):
    def get_item_by_id(self, pk):
        """
        Получение жанров по id
        :param pk: id жанра
        :return: данные о жанре в формате json
        """
        genre = GenreDAO(self._db_session).get_by_id(pk)
        if not genre:
            raise ItemNotFound
        return GenreSchema().dump(genre)

    def get_all_genres(self):
        """
        Получение всех жанров
        :return: все жанры в json формате
        """
        genres = GenreDAO(self._db_session).get_all()
        return GenreSchema(many=True).dump(genres)