import base64
import os

from src import db
from src.models import User, Region, Boulder, Send

SEED_IMAGES_DIR = os.path.join(os.path.dirname(__file__), "seed_images")


def load_seed_image(filename):
    path = os.path.join(SEED_IMAGES_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        data = f.read()
    ext = os.path.splitext(filename)[1].lstrip(".").lower()
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{base64.b64encode(data).decode()}"


def seed_data():
    created = {
        "users": 0,
        "regions": 0,
        "boulders": 0,
        "sends": 0,
    }

    updated = {
        "users": 0,
        "regions": 0,
        "boulders": 0,
        "sends": 0,
    }

    user_1 = db.session.execute(
        db.select(User).where(User.username == "kyle")
    ).scalar_one_or_none()

    if user_1 is None:
        user_1 = User(username="kyle", display_name="Kyle")
        db.session.add(user_1)
        created["users"] += 1
    else:
        user_1.display_name = "Kyle"
        updated["users"] += 1

    user_2 = db.session.execute(
        db.select(User).where(User.username == "sam")
    ).scalar_one_or_none()

    if user_2 is None:
        user_2 = User(username="sam", display_name="Sam")
        db.session.add(user_2)
        created["users"] += 1
    else:
        user_2.display_name = "Sam"
        updated["users"] += 1

    db.session.flush()

    region_1 = db.session.execute(
        db.select(Region).where(
            Region.type == "country",
            Region.name == "canada",
        )
    ).scalar_one_or_none()

    if region_1 is None:
        region_1 = Region(type="country", name="canada", parent_id=None)
        db.session.add(region_1)
        created["regions"] += 1
    else:
        region_1.parent_id = None
        updated["regions"] += 1

    db.session.flush()

    region_2 = db.session.execute(
        db.select(Region).where(
            Region.type == "province",
            Region.name == "british columbia",
        )
    ).scalar_one_or_none()

    if region_2 is None:
        region_2 = Region(
            type="province",
            name="british columbia",
            parent_id=region_1.id,
        )
        db.session.add(region_2)
        created["regions"] += 1
    else:
        region_2.parent_id = region_1.id
        updated["regions"] += 1

    db.session.flush()


    region_3 = db.session.execute(
        db.select(Region).where(
            Region.type == "city",
            Region.name == "Nanaimo",
        )
    ).scalar_one_or_none()

    if region_3 is None:
        region_3 = Region(
            type="city",
            name="Nanaimo",
            parent_id=region_2.id,
        )
        db.session.add(region_3)
        created["regions"] += 1
    else:
        region_3.parent_id = region_2.id
        updated["regions"] += 1

    db.session.flush()

    region_4 = db.session.execute(
        db.select(Region).where(
            Region.type == "country",
            Region.name == "Finland",
        )
    ).scalar_one_or_none()

    if region_4 is None:
        region_4 = Region(
            type="country",
            name="Finland",
            parent_id=None,
        )
        db.session.add(region_4)
        created["regions"] += 1
    else:
        region_4.parent_id = None
        updated["regions"] += 1

    db.session.flush()
       

    seed_boulders = [
        {
            "name": "the egg",
            "author": user_1,
            "region": region_2,
            "description": "short powerful roof climb",
            "grade": 5,
            "coordinates": "48.778,-123.707",
            "image": load_seed_image("the_egg.jpg"),
        },
        {
            "name": "granite dream",
            "author": user_2,
            "region": region_2,
            "description": "technical face with small crimps",
            "grade": 7,
            "coordinates": "48.800,-123.690",
            "image": None,
        },
        {
            "name": "Wip Climbing",
            "author": user_2,
            "region": region_2,
            "description": "Cllimbing gym in nanaimo",
            "grade": 5,
            "coordinates": "49.1822632, -123.9844017",
            "image": load_seed_image("wip_climbing.jpg"),
        }
    ]

    boulder_objects = []
    for b in seed_boulders:
        existing = db.session.execute(
            db.select(Boulder).where(
                Boulder.name == b["name"],
                Boulder.author_id == b["author"].id,
            )
        ).scalar_one_or_none()

        if existing is None:
            existing = Boulder(
                author_id=b["author"].id,
                region_id=b["region"].id,
                name=b["name"],
                description=b["description"],
                image=b.get("image"),
                grade=b["grade"],
                coordinates=b["coordinates"],
            )
            db.session.add(existing)
            created["boulders"] += 1
        else:
            existing.region_id = b["region"].id
            existing.description = b["description"]
            existing.grade = b["grade"]
            existing.coordinates = b["coordinates"]
            if b.get("image") is not None:
                existing.image = b["image"]
            updated["boulders"] += 1

        boulder_objects.append(existing)

    db.session.flush()

    seed_sends = [
        {"boulder": boulder_objects[0], "user": user_2, "rating": 4.5, "send_type": 1},
        {"boulder": boulder_objects[1], "user": user_1, "rating": 5.0, "send_type": 2},
    ]

    for s in seed_sends:
        existing = db.session.execute(
            db.select(Send).where(
                Send.boulder_id == s["boulder"].id,
                Send.user_id == s["user"].id,
            )
        ).scalar_one_or_none()

        if existing is None:
            existing = Send(
                boulder_id=s["boulder"].id,
                user_id=s["user"].id,
                rating=s["rating"],
                send_type=s["send_type"],
            )
            db.session.add(existing)
            created["sends"] += 1
        else:
            existing.rating = s["rating"]
            existing.send_type = s["send_type"]
            updated["sends"] += 1

    db.session.commit()

    return {
        "message": "seed completed",
        "created": created,
        "updated": updated,
    }