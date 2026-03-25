from flask import Blueprint, jsonify

from src.services.seeder import seed_data

seed_blueprint = Blueprint("seed", __name__)


@seed_blueprint.get("/")
def seed():
    print("----- SEEDING -----")
    result = seed_data()
    return jsonify(result), 200