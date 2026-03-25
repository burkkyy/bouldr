from datetime import datetime

from flask import Blueprint, jsonify, request

from src import db
from src.models import Region

regions_blueprint = Blueprint("regions", __name__)


def serialize_region(region: Region) -> dict:
    return {
        "id": region.id,
        "type": region.type,
        "name": region.name,
        "parentID": region.parent_id,
        "createdAt": region.created_at.isoformat() if region.created_at else None,
        "updatedAt": region.updated_at.isoformat() if region.updated_at else None,
        "deletedAt": region.deleted_at.isoformat() if region.deleted_at else None,
    }


def get_active_region(id: int) -> Region | None:
    return db.session.execute(
        db.select(Region).where(Region.id == id, Region.deleted_at.is_(None))
    ).scalar_one_or_none()


@regions_blueprint.get("/")
def index():
    regions = db.session.execute(
        db.select(Region).where(Region.deleted_at.is_(None))
    ).scalars().all()

    return jsonify([serialize_region(region) for region in regions])


@regions_blueprint.get("/<int:id>")
def get(id):
    region = get_active_region(id)

    if region is None:
        return jsonify({"error": "region not found"}), 404

    return jsonify(serialize_region(region))


@regions_blueprint.post("/")
def create():
    data = request.get_json(silent=True) or {}

    region_type = data.get("type")
    name = data.get("name")
    parent_id = data.get("parentID")

    if not region_type:
        return jsonify({"error": "type is required"}), 400

    if not name:
        return jsonify({"error": "name is required"}), 400

    if parent_id is not None and get_active_region(parent_id) is None:
        return jsonify({"error": "parent region not found"}), 400

    region = Region(
        type=region_type.lower(),
        name=name,
        parent_id=parent_id,
    )

    db.session.add(region)
    db.session.commit()

    return jsonify(serialize_region(region)), 201


@regions_blueprint.patch("/<int:id>")
def update(id):
    region = get_active_region(id)

    if region is None:
        return jsonify({"error": "region not found"}), 404

    data = request.get_json(silent=True) or {}

    if "type" in data:
        if not data["type"]:
            return jsonify({"error": "type cannot be empty"}), 400
        region.type = data["type"].lower()

    if "name" in data:
        if not data["name"]:
            return jsonify({"error": "name cannot be empty"}), 400
        region.name = data["name"]

    if "parentID" in data:
        parent_id = data["parentID"]

        if parent_id == id:
            return jsonify({"error": "region cannot be its own parent"}), 400

        if parent_id is not None and get_active_region(parent_id) is None:
            return jsonify({"error": "parent region not found"}), 400

        region.parent_id = parent_id

    db.session.commit()

    return jsonify(serialize_region(region))


@regions_blueprint.delete("/<int:id>")
def delete(id):
    region = get_active_region(id)

    if region is None:
        return jsonify({"error": "region not found"}), 404

    region.deleted_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "region deleted"})