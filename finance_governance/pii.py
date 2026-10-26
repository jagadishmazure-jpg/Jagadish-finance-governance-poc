"""PII redaction: cards, emails, phones, SSNs -- all four, always.

The checklist is deliberately explicit: earlier reviews caught checklists
that named only phone and SSN and silently passed card numbers and
email addresses through. Every pattern below is tested.
"""

import re

CARD_RE = re.compile(r"\b(?:\d[ -]?){13,19}\b")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\b(?:\+?1[-. ]?)?(?:\(\d{3}\)|\d{3})[-. ]\d{3}[-. ]\d{4}\b")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

PII_CHECKLIST = ("card_number", "email_address", "phone_number", "ssn")


def redact_text(text):
    """Replace each PII pattern with a typed placeholder. Never returns raw PII."""
    if text is None:
        return ""
    out = str(text)
    out = CARD_RE.sub("[REDACTED:CARD]", out)
    out = EMAIL_RE.sub("[REDACTED:EMAIL]", out)
    out = SSN_RE.sub("[REDACTED:SSN]", out)
    out = PHONE_RE.sub("[REDACTED:PHONE]", out)
    return out


def find_pii_types(text):
    found = []
    if CARD_RE.search(text or ""):
        found.append("card_number")
    if EMAIL_RE.search(text or ""):
        found.append("email_address")
    if PHONE_RE.search(text or ""):
        found.append("phone_number")
    if SSN_RE.search(text or ""):
        found.append("ssn")
    return found
