import re
from functools import wraps

from flask import jsonify, request, g

from src import db
from src.models import User

PASSWORD_RE = re.compile(r'^(?=.*[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]).{8,}$')


def validate_password(password: str) -> str | None:
    if not password or len(password) < 8:
        return "Password must be at least 8 characters long"
    if not PASSWORD_RE.match(password):
        return "Password must contain at least one special character"
    return None


def get_current_user() -> User | None:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    try:
        user_id = int(auth_header.split(" ")[1])
    except (ValueError, IndexError):
        return None

    return db.session.execute(
        db.select(User).where(User.id == user_id, User.deleted_at.is_(None))
    ).scalar_one_or_none()


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if user is None:
            return jsonify({"error": "Authentication required"}), 401
        g.current_user = user
        return f(*args, **kwargs)
    return decorated
