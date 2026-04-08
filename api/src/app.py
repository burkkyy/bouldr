import os

from flask import Flask, send_from_directory
from flask_cors import CORS

from src import db
from src.config import Config
from src.blueprints import register_blueprints


def create_app():
    static_dir = os.path.join(os.path.dirname(__file__), "web")
    app = Flask(__name__, static_folder=static_dir, static_url_path="/web")
    app.config.from_object(Config)

    CORS(
        app,
        origins=Config.FRONTEND_URLS,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    )

    db.init_app(app)

    with app.app_context():
        from src import models
        db.create_all()  # only creates missing tables

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
