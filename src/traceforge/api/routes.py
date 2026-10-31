"""Small helpers shared by the stdlib HTTP route handlers."""

from urllib.parse import parse_qs, urlparse


def pagination(path: str, default_limit: int = 100) -> tuple[int, int]:
    """Parse bounded `limit` and nonnegative `offset` query parameters."""
    query = parse_qs(urlparse(path).query)
    try:
        limit = int(query.get("limit", [str(default_limit)])[0])
        offset = int(query.get("offset", ["0"])[0])
    except ValueError:
        raise ValueError("limit and offset must be integers") from None
    if limit < 1 or offset < 0:
        raise ValueError("limit must be positive and offset nonnegative")
    return min(limit, 500), offset
