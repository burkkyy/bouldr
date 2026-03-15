from typing import Optional


DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 20
MAX_PER_PAGE = 100


def parse_int(
    value,
    default: int,
    minimum: int = 1,
    maximum: Optional[int] = None,
) -> int:
    try:
        parsed_value = int(value)
    except (TypeError, ValueError):
        return default

    if parsed_value < minimum:
        return default

    if maximum is not None and parsed_value > maximum:
        return maximum

    return parsed_value


def parse_optional_int(value) -> Optional[int]:
    if value is None or value == "":
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_bool(value) -> Optional[bool]:
    if value is None:
        return None

    normalized_value = str(value).strip().lower()

    if normalized_value in {"true", "1", "yes"}:
        return True

    if normalized_value in {"false", "0", "no"}:
        return False

    return None


def parse_pagination(args):
    page = parse_int(args.get("page"), DEFAULT_PAGE)
    per_page = parse_int(
        args.get("perPage"),
        DEFAULT_PER_PAGE,
        maximum=MAX_PER_PAGE,
    )

    return page, per_page


def build_page_response(page_obj):
    return {
        "items": [item.to_dict() for item in page_obj.items],
        "pagination": {
            "page": page_obj.page,
            "perPage": page_obj.per_page,
            "total": page_obj.total,
            "pages": page_obj.pages,
            "hasNext": page_obj.has_next,
            "hasPrev": page_obj.has_prev,
        },
    }