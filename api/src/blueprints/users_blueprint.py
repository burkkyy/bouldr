from flask import Blueprint, jsonify

from src import db
from src.models import User

users_blueprint = Blueprint("users", __name__)

@users_blueprint.get("/")
def index():
    users = db.session.execute(db.select(User)).scalars().all()
    return jsonify([{"id": user.id, "username": user.username} for user in users])

@users_blueprint.get("/<int:id>")
def get(id):
    user = db.get_or_404(User, id)
    return jsonify({"id": user.id, "username": user.username})

@users_blueprint.post("/")
def create():
    raise NotImplementedError("Not Implemented")

@users_blueprint.patch("/<int:id>")
def update(id):
    raise NotImplementedError("Not Implemented")

@users_blueprint.delete("/<int:id>")
def delete(id):
    raise NotImplementedError("Not Implemented")
