from src import db
from src.models import User, Region, Boulder, Send


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

    boulder_1 = db.session.execute(
        db.select(Boulder).where(
            Boulder.name == "the egg",
            Boulder.author_id == user_1.id,
        )
    ).scalar_one_or_none()

    if boulder_1 is None:
        boulder_1 = Boulder(
            author_id=user_1.id,
            name="the egg",
            description="short powerful roof climb",
            image="https://example.com/egg.jpg",
            grade=5,
            coordinates="48.778,-123.707",
        )
        db.session.add(boulder_1)
        created["boulders"] += 1
    else:
        boulder_1.description = "short powerful roof climb"
        boulder_1.image = "https://example.com/egg.jpg"
        boulder_1.grade = 5
        boulder_1.coordinates = "48.778,-123.707"
        updated["boulders"] += 1

    boulder_2 = db.session.execute(
        db.select(Boulder).where(
            Boulder.name == "granite dream",
            Boulder.author_id == user_2.id,
        )
    ).scalar_one_or_none()

    if boulder_2 is None:
        boulder_2 = Boulder(
            author_id=user_2.id,
            name="granite dream",
            description="technical face with small crimps",
            image="https://example.com/granite.jpg",
            grade=7,
            coordinates="48.800,-123.690",
        )
        db.session.add(boulder_2)
        created["boulders"] += 1
    else:
        boulder_2.description = "technical face with small crimps"
        boulder_2.image = "https://example.com/granite.jpg"
        boulder_2.grade = 7
        boulder_2.coordinates = "48.800,-123.690"
        updated["boulders"] += 1

    db.session.flush()

    send_1 = db.session.execute(
        db.select(Send).where(
            Send.boulder_id == boulder_1.id,
            Send.user_id == user_2.id,
        )
    ).scalar_one_or_none()

    if send_1 is None:
        send_1 = Send(
            boulder_id=boulder_1.id,
            user_id=user_2.id,
            rating=4.5,
            send_type=1,
        )
        db.session.add(send_1)
        created["sends"] += 1
    else:
        send_1.rating = 4.5
        send_1.send_type = 1
        updated["sends"] += 1

    send_2 = db.session.execute(
        db.select(Send).where(
            Send.boulder_id == boulder_2.id,
            Send.user_id == user_1.id,
        )
    ).scalar_one_or_none()

    if send_2 is None:
        send_2 = Send(
            boulder_id=boulder_2.id,
            user_id=user_1.id,
            rating=5.0,
            send_type=2,
        )
        db.session.add(send_2)
        created["sends"] += 1
    else:
        send_2.rating = 5.0
        send_2.send_type = 2
        updated["sends"] += 1

    db.session.commit()

    return {
        "message": "seed completed",
        "created": created,
        "updated": updated,
    }