from coursework_3_source.project.dao.director import DirectorDAO
from coursework_3_source.project.dao.genre import GenreDAO
from coursework_3_source.project.dao.movie import MovieDAO
from coursework_3_source.project.dao.user import UserDAO
from coursework_3_source.project.services.directors_service import DirectorsService
from coursework_3_source.project.services.genres_service import GenresService
from coursework_3_source.project.services.movies_service import MoviesService

# from coursework_3_source.project.services.user import UserService
from coursework_3_source.project.setup_db import db

director_dao = DirectorDAO(session=db.session)
genre_dao = GenreDAO(session=db.session)
movie_dao = MovieDAO(session=db.session)
user_dao = UserDAO(session=db.session)

director_service = DirectorsService(dao=director_dao)
genre_service = GenresService(dao=genre_dao)
movie_service = MoviesService(dao=movie_dao)
# user_service = UsersService(dao=user_dao)
