from flask_sqlalchemy import SQLAlchemy


class DB:
    session = None

    @classmethod
    def init(cls, app):
        db = SQLAlchemy()
        db.init_app(app)
        db.app = app
        db.create_all()
        cls.session = db.session
