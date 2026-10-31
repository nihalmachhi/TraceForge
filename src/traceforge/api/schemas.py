"""Typed payloads returned by the local HTTP API."""

from typing import NotRequired, TypedDict


class HealthResponse(TypedDict):
    """Health response for the synthetic local service."""

    status: str
    data_mode: str


class PageResponse(TypedDict):
    """Paginated trace-list response."""

    items: list[dict[str, object]]
    limit: int
    offset: int
    next_offset: NotRequired[int | None]
