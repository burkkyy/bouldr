import base64
import re
from datetime import datetime

from flask import Blueprint, Response, g, jsonify, request

from src import db
from src.models import Boulder, User
from src.auth import require_auth

COORDINATES_RE = re.compile(
    r"^-?(?:[1-8]?\d(?:\.\d+)?|90(?:\.0+)?),\s*-?(?:1[0-7]\d(?:\.\d+)?|180(?:\.0+)?|\d{1,2}(?:\.\d+)?)$"
)

boulders_blueprint = Blueprint("boulders", __name__)


def serialize_boulder(boulder: Boulder) -> dict:
    return {
        "id": boulder.id,
        "authorID": boulder.author_id,
        "regionID": boulder.region_id,
        "name": boulder.name,
        "description": boulder.description,
        "image": boulder.image,
        "grade": boulder.grade,
        "coordinates": boulder.coordinates,
        "createdAt": boulder.created_at.isoformat() if boulder.created_at else None,
        "updatedAt": boulder.updated_at.isoformat() if boulder.updated_at else None,
        "deletedAt": boulder.deleted_at.isoformat() if boulder.deleted_at else None,
    }


def get_active_boulder(id: int) -> Boulder | None:
    return db.session.execute(
        db.select(Boulder).where(Boulder.id == id, Boulder.deleted_at.is_(None))
    ).scalar_one_or_none()


def get_active_user(id: int) -> User | None:
    return db.session.execute(
        db.select(User).where(User.id == id, User.deleted_at.is_(None))
    ).scalar_one_or_none()


@boulders_blueprint.get("/")
def index():
    query = db.select(Boulder).where(Boulder.deleted_at.is_(None))

    region_id = request.args.get("regionId")
    if region_id is not None:
        query = query.where(Boulder.region_id == int(region_id))

    boulders = db.session.execute(query).scalars().all()

    return jsonify([serialize_boulder(boulder) for boulder in boulders])


@boulders_blueprint.get("/<int:id>")
def get(id):
    boulder = get_active_boulder(id)

    if boulder is None:
        return jsonify({"error": "boulder not found"}), 404

    return jsonify(serialize_boulder(boulder))


@boulders_blueprint.get("/<int:id>/image")
def get_image(id):
    boulder = get_active_boulder(id)

    if boulder is None:
        return jsonify({"error": "boulder not found"}), 404

    if not boulder.image:
        return jsonify({"error": "boulder has no image"}), 404

    # Parse data URL: "data:image/png;base64,<data>"
    match = re.match(r"data:image/(\w+);base64,(.+)", boulder.image)
    if not match:
        return jsonify({"error": "invalid image data"}), 500

    mime_type = f"image/{match.group(1)}"
    image_bytes = base64.b64decode(match.group(2))

    return Response(image_bytes, content_type=mime_type)


@boulders_blueprint.post("/")
def create():
    data = request.get_json(silent=True) or {}

    author_id = data.get("authorID")
    name = data.get("name")
    grade = data.get("grade")

    if author_id is None:
        return jsonify({"error": "authorID is required"}), 400

    if not name:
        return jsonify({"error": "name is required"}), 400

    if grade is None:
        return jsonify({"error": "grade is required"}), 400

    if get_active_user(author_id) is None:
        return jsonify({"error": "author not found"}), 400

    coordinates = data.get("coordinates")
    if coordinates and not COORDINATES_RE.match(coordinates.strip()):
        return jsonify({"error": "coordinates must be in 'lat, lng' format (e.g. 49.123, -123.456)"}), 400

    boulder = Boulder(
        author_id=author_id,
        region_id=data.get("regionID"),
        name=name,
        description=data.get("description"),
        image=data.get("image"),
        grade=grade,
        coordinates=coordinates.strip() if coordinates else None,
    )

    db.session.add(boulder)
    db.session.commit()

    return jsonify(serialize_boulder(boulder)), 201


@boulders_blueprint.patch("/<int:id>")
@require_auth
def update(id):
    boulder = get_active_boulder(id)

    if boulder is None:
        return jsonify({"error": "boulder not found"}), 404

    if boulder.author_id != g.current_user.id:
        return jsonify({"error": "You can only edit your own boulders"}), 403

    data = request.get_json(silent=True) or {}

    if "authorID" in data:
        author_id = data["authorID"]

        if get_active_user(author_id) is None:
            return jsonify({"error": "author not found"}), 400

        boulder.author_id = author_id

    if "regionID" in data:
        boulder.region_id = data["regionID"]

    if "name" in data:
        if not data["name"]:
            return jsonify({"error": "name cannot be empty"}), 400
        boulder.name = data["name"]

    if "description" in data:
        boulder.description = data["description"]

    if "image" in data:
        boulder.image = data["image"]

    if "grade" in data:
        if data["grade"] is None:
            return jsonify({"error": "grade cannot be null"}), 400
        boulder.grade = data["grade"]

    if "coordinates" in data:
        if data["coordinates"] and not COORDINATES_RE.match(data["coordinates"].strip()):
            return jsonify({"error": "coordinates must be in 'lat, lng' format (e.g. 49.123, -123.456)"}), 400
        boulder.coordinates = data["coordinates"].strip() if data["coordinates"] else None

    db.session.commit()

    return jsonify(serialize_boulder(boulder))


@boulders_blueprint.delete("/<int:id>")
@require_auth
def delete(id):
    boulder = get_active_boulder(id)

    if boulder is None:
        return jsonify({"error": "boulder not found"}), 404

    if boulder.author_id != g.current_user.id:
        return jsonify({"error": "You can only delete your own boulders"}), 403

    boulder.deleted_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "boulder deleted"})