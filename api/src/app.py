from flask import Flask

from src import db
from src.config import Config
from src.blueprints import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URL
    
    db.init_app(app)

    with app.app_context():
        from src import models
        db.create_all() # NOTE: Only creates tables if they dont exist

    register_blueprints(app)
    return app


if __name__ == "__main__":
    app = create_app()
