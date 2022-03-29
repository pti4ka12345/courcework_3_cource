from flask import current_app
from sqlalchemy.orm import scoped_session

from coursework_3_source.project.dao.models.movie import MovieSchema
from coursework_3_source.project.dao.movie import MovieDAO
from coursework_3_source.project.exceptions import ItemNotFound
from coursework_3_source.project.services.base import BaseService


class MoviesService(BaseService):
    def __init__(self, session: scoped_session):
        super().__init__(session)
        self.dao = None

    def get_item_by_id(self, pk):
        movie = MovieDAO(self._db_session).get_by_id(pk)
        if not movie:
            raise ItemNotFound
        return MovieSchema().dump(movie)

    def get_all_movies(self):
        movies = MovieDAO(self._db_session).get_all()
        return MovieSchema(many=True).dump(movies)

    def get_filter_movies(self, filters):
        limit = 0
        offset = 0
        if filters.get("page"):
            limit = current_app.config["ITEMS_PER_PAGE"]
            offset = (filters.get("page") - 1) * limit
        status = filters.get("status")
        movies = MovieDAO(self._db_session).get_filter(limit=limit, offset=offset, status=status)
        return MovieSchema(many=True).dump(movies)
