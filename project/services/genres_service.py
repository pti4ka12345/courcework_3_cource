from coursework_3_source.project.dao.genre import GenreDAO
from coursework_3_source.project.dao.models.genre import GenreSchema
from coursework_3_source.project.exceptions import ItemNotFound
from coursework_3_source.project.services.base import BaseService


class GenresService(BaseService):
    def get_item_by_id(self, pk):
        genre = GenreDAO(self._db_session).get_by_id(pk)
        if not genre:
            raise ItemNotFound
        return GenreSchema().dump(genre)

    def get_all_genres(self):
        genres = GenreDAO(self._db_session).get_all()
        return GenreSchema(many=True).dump(genres)
