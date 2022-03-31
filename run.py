from coursework_3_source.project.dao.models import Director, Movie, User
from project.config import DevelopmentConfig
from project.dao.models import Genre
from project.server import create_app, db

app = create_app(DevelopmentConfig)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "Movie": Movie,
        "User": User,
    }
