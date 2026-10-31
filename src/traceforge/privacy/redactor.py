"""Best-effort recursive masking of sensitive keys and free-text values."""

import re
from collections.abc import Collection

from traceforge.privacy.patterns import (
    AWS_KEY,
    BEARER,
    CARD_CANDIDATE,
    EMAIL,
    JWT,
    PHONE_CANDIDATE,
    SECRET_TOKEN,
    SENSITIVE_KEY,
    SSN,
    passes_luhn,
)

MASK = "[REDACTED]"
DEFAULT_ALLOWLIST = frozenset({"author", "tokenizer", "token_count", "email_domain"})
_TEXT_PATTERNS = (EMAIL, SSN, JWT, BEARER, SECRET_TOKEN, AWS_KEY)


def _key_is_sensitive(key: str, allowlist: Collection[str]) -> bool:
    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", key).lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")
    if normalized in allowlist:
        return False
    return SENSITIVE_KEY.search(key) is not None


def _redact_text(value: str) -> str:
    for pattern in _TEXT_PATTERNS:
        value = pattern.sub(MASK, value)
    value = PHONE_CANDIDATE.sub(
        lambda match: (
            MASK if sum(character.isdigit() for character in match.group()) >= 10 else match.group()
        ),
        value,
    )
    return CARD_CANDIDATE.sub(
        lambda match: MASK if passes_luhn(match.group()) else match.group(), value
    )


def redact(
    value: object,
    key: str = "",
    *,
    allowlist: Collection[str] | None = None,
) -> object:
    """Mask sensitive keys and common secrets while preserving container shape.

    This is a best-effort safeguard; it cannot detect every form of personal data.
    """
    allowed = DEFAULT_ALLOWLIST if allowlist is None else allowlist
    sensitive = bool(key) and _key_is_sensitive(key, allowed)
    if sensitive and not isinstance(value, (dict, list, tuple)):
        return MASK
    if isinstance(value, dict):
        return {
            str(item_key): redact(
                item,
                key if sensitive else str(item_key),
                allowlist=allowed,
            )
            for item_key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [redact(item, key if sensitive else "", allowlist=allowed) for item in value]
    if isinstance(value, str):
        return _redact_text(value)
    return value
