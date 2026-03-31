from datetime import datetime

from flask import Blueprint, jsonify, request

from src import db
from src.models import User

users_blueprint = Blueprint("users", __name__)


def serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "displayName": user.display_name,
        "createdAt": user.created_at.isoformat() if user.created_at else None,
        "updatedAt": user.updated_at.isoformat() if user.updated_at else None,
        "deletedAt": user.deleted_at.isoformat() if user.deleted_at else None,
    }


def get_active_user(id: int) -> User | None:
    return db.session.execute(
        db.select(User).where(User.id == id, User.deleted_at.is_(None))
    ).scalar_one_or_none()


@users_blueprint.get("/")
def index():
    query = db.select(User).where(User.deleted_at.is_(None))

    username = request.args.get("username")
    if username is not None:
        query = query.where(User.username == username)

    users = db.session.execute(query).scalars().all()

    return jsonify([serialize_user(user) for user in users])


@users_blueprint.get("/<int:id>")
def get(id):
    user = get_active_user(id)

    if user is None:
        return jsonify({"error": "user not found"}), 404

    return jsonify(serialize_user(user))


@users_blueprint.post("/")
def create():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    if not username:
        return jsonify({"error": "username is required"}), 400

    user = User(
        username=username,
        display_name=data.get("displayName"),
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(serialize_user(user)), 201


@users_blueprint.patch("/<int:id>")
def update(id):
    user = get_active_user(id)

    if user is None:
        return jsonify({"error": "user not found"}), 404

    data = request.get_json(silent=True) or {}

    if "username" in data:
        if not data["username"]:
            return jsonify({"error": "username cannot be empty"}), 400
        user.username = data["username"]

    if "displayName" in data:
        user.display_name = data["displayName"]

    db.session.commit()

    return jsonify(serialize_user(user))


@users_blueprint.delete("/<int:id>")
def delete(id):
    user = get_active_user(id)

    if user is None:
        return jsonify({"error": "user not found"}), 404

    user.deleted_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "user deleted"})