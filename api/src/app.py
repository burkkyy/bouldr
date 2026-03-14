import os

from flask import Flask, send_from_directory

from src import db
from src.config import Config
from src.blueprints import register_blueprints

def create_app():
    app = Flask(__name__, static_folder="web", static_url_path="")
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URL
    
    db.init_app(app)

    with app.app_context():
        from src import models
        db.create_all() # NOTE: Only creates tables if they dont exist

    register_blueprints(app)

    # If api didn't match, serve frontend
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def fallback(path):
        return send_from_directory(app.static_folder, "index.html")

    return app


if __name__ == "__main__":
    app = create_app()

    if Config.NODE_ENV == "production":
        app.run(host="0.0.0.0", port=Config.API_PORT)
    elif Config.NODE_ENV == "development":
        app.run(host="0.0.0.0", port=Config.API_PORT, debug=True)
