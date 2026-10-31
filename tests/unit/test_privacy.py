from traceforge.privacy.patterns import passes_luhn
from traceforge.privacy.redactor import MASK, redact


def test_redacts_lists_without_losing_parent_key() -> None:
    assert redact({"emails": ["person@example.com"]}) == {"emails": [MASK]}


def test_redacts_text_and_preserves_safe_keys() -> None:
    result = redact({"author": "person@example.com", "tokenizer": "simple"})
    assert result == {"author": MASK, "tokenizer": "simple"}


def test_allowlist_override_is_supported() -> None:
    assert redact({"token": "ordinary text"}, allowlist={"token"}) == {"token": "ordinary text"}


def test_redacts_common_secrets_and_only_luhn_valid_cards() -> None:
    message = "person@example.com 123-45-6789 Bearer abcdef123456 sk-live_abcdefghijkl"
    assert MASK in redact(message)
    assert passes_luhn("4111 1111 1111 1111")
    assert not passes_luhn("4111 1111 1111 1112")
