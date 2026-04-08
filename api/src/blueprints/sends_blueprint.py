from datetime import datetime

from flask import Blueprint, g, jsonify, request

from src import db
from src.models import Boulder, Send, User
from src.auth import require_auth

sends_blueprint = Blueprint("sends", __name__)


def serialize_send(send: Send, user: User | None = None) -> dict:
    data = {
        "id": send.id,
        "boulderID": send.boulder_id,
        "userID": send.user_id,
        "rating": send.rating,
        "sendType": send.send_type,
        "createdAt": send.created_at.isoformat() if send.created_at else None,
        "updatedAt": send.updated_at.isoformat() if send.updated_at else None,
        "deletedAt": send.deleted_at.isoformat() if send.deleted_at else None,
    }
    if user is not None:
        data["username"] = user.username
        data["displayName"] = user.display_name
    return data


def get_active_send(id: int) -> Send | None:
    return db.session.execute(
        db.select(Send).where(Send.id == id, Send.deleted_at.is_(None))
    ).scalar_one_or_none()


def get_active_boulder(id: int) -> Boulder | None:
    return db.session.execute(
        db.select(Boulder).where(Boulder.id == id, Boulder.deleted_at.is_(None))
    ).scalar_one_or_none()


def get_active_user(id: int) -> User | None:
    return db.session.execute(
        db.select(User).where(User.id == id, User.deleted_at.is_(None))
    ).scalar_one_or_none()


@sends_blueprint.get("/")
def index():
    query = db.select(Send).where(Send.deleted_at.is_(None))

    boulder_id = request.args.get("boulderID")
    if boulder_id is not None:
        query = query.where(Send.boulder_id == int(boulder_id))

    sends = db.session.execute(query).scalars().all()

    # Build a map of user_ids to users for the response
    user_ids = {s.user_id for s in sends}
    users = {}
    if user_ids:
        user_rows = db.session.execute(
            db.select(User).where(User.id.in_(user_ids))
        ).scalars().all()
        users = {u.id: u for u in user_rows}

    return jsonify([serialize_send(send, users.get(send.user_id)) for send in sends])


@sends_blueprint.get("/<int:id>")
def get(id):
    send = get_active_send(id)

    if send is None:
        return jsonify({"error": "send not found"}), 404

    return jsonify(serialize_send(send))


@sends_blueprint.post("/")
def create():
    data = request.get_json(silent=True) or {}

    boulder_id = data.get("boulderID")
    user_id = data.get("userID")
    send_type = data.get("sendType")

    if boulder_id is None:
        return jsonify({"error": "boulderID is required"}), 400

    if user_id is None:
        return jsonify({"error": "userID is required"}), 400

    if send_type is None:
        return jsonify({"error": "sendType is required"}), 400

    if get_active_boulder(boulder_id) is None:
        return jsonify({"error": "boulder not found"}), 400

    if get_active_user(user_id) is None:
        return jsonify({"error": "user not found"}), 400

    send = Send(
        boulder_id=boulder_id,
        user_id=user_id,
        rating=data.get("rating"),
        send_type=send_type,
    )

    db.session.add(send)
    db.session.commit()

    return jsonify(serialize_send(send)), 201


@sends_blueprint.patch("/<int:id>")
@require_auth
def update(id):
    send = get_active_send(id)

    if send is None:
        return jsonify({"error": "send not found"}), 404

    if send.user_id != g.current_user.id:
        return jsonify({"error": "You can only edit your own sends"}), 403

    data = request.get_json(silent=True) or {}

    if "boulderID" in data:
        boulder_id = data["boulderID"]

        if get_active_boulder(boulder_id) is None:
            return jsonify({"error": "boulder not found"}), 400

        send.boulder_id = boulder_id

    if "userID" in data:
        user_id = data["userID"]

        if get_active_user(user_id) is None:
            return jsonify({"error": "user not found"}), 400

        send.user_id = user_id

    if "rating" in data:
        send.rating = data["rating"]

    if "sendType" in data:
        if data["sendType"] is None:
            return jsonify({"error": "sendType cannot be null"}), 400
        send.send_type = data["sendType"]

    db.session.commit()

    return jsonify(serialize_send(send))


@sends_blueprint.delete("/<int:id>")
@require_auth
def delete(id):
    send = get_active_send(id)

    if send is None:
        return jsonify({"error": "send not found"}), 404

    if send.user_id != g.current_user.id:
        return jsonify({"error": "You can only delete your own sends"}), 403

    send.deleted_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "send deleted"})