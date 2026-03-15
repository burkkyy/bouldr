from flask import Blueprint, jsonify

from src.services.seeder import seed_data

seed_blueprint = Blueprint("seed", __name__)


@seed_blueprint.post("/seed")
def seed():
    result = seed_data()
    return jsonify(result), 200