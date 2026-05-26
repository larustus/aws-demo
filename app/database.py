import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Database(SQLAlchemy):
    def database_uri(self) -> str:
        db_path = os.environ.get("DB_PATH")
        if db_path:
            path = Path(db_path).expanduser()
        else:
            path = Path(__file__).resolve().parent.parent / "comments.db"

        return f"sqlite:///{path.as_posix()}"


db = Database()


def init_db(app: Flask) -> None:
    with app.app_context():
        db.create_all()
