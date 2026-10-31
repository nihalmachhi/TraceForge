"""Sensitive-value patterns used by the best-effort redactor."""

import re

SENSITIVE_KEY = re.compile(
    r"(?:^|[_\W])(?:api[_-]?keys?|access[_-]?tokens?|auth(?:orization)?|tokens?|secrets?|"
    r"passwords?|passwds?|emails?|phones?|mobiles?|ssns?|social[_-]?security[_-]?numbers?|"
    r"credit[_-]?card|card[_-]?number)(?:$|[_\W])",
    re.IGNORECASE,
)
EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
SSN = re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")
JWT = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
BEARER = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]+=*")
SECRET_TOKEN = re.compile(r"\b(?:sk|rk|pk)-[A-Za-z0-9_-]{12,}\b")
AWS_KEY = re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")
CARD_CANDIDATE = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")
PHONE_CANDIDATE = re.compile(r"(?<!\w)(?:\+?\d[\d .()/-]{8,}\d)(?!\w)")


def passes_luhn(value: str) -> bool:
    """Return whether a digit sequence passes the Luhn checksum."""
    digits = [int(character) for character in value if character.isdigit()]
    if not 13 <= len(digits) <= 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0
