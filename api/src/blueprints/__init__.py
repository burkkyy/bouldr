from src.blueprints.users_blueprint import users_blueprint

def register_blueprints(app):
    app.register_blueprint(users_blueprint, url_prefix="/api/users")