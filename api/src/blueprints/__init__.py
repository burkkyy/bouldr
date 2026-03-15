from src.blueprints.users_blueprint import users_blueprint
from src.blueprints.regions_blueprint import regions_blueprint
from src.blueprints.boulders_blueprint import boulders_blueprint
from src.blueprints.sends_blueprint import sends_blueprint
from src.blueprints.seed_blueprint import seed_blueprint


def register_blueprints(app):
    app.register_blueprint(users_blueprint, url_prefix="/api/users")
    app.register_blueprint(regions_blueprint, url_prefix="/api/regions")
    app.register_blueprint(boulders_blueprint, url_prefix="/api/boulders")
    app.register_blueprint(sends_blueprint, url_prefix="/api/sends")
    app.register_blueprint(seed_blueprint, url_prefix="/api")
