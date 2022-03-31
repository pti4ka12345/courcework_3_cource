from coursework_3_source.project.views.auth import auth_ns
from coursework_3_source.project.views.directors import directors_ns
from coursework_3_source.project.views.movies import movies_ns
from coursework_3_source.project.views.users import user_ns
from coursework_3_source.project.views.genres import genres_ns

__all__ = [
    "genres_ns", "directors_ns", "movies_ns", "user_ns", "auth_ns",
]
