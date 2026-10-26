"""Confirmation gates: bypass, reject, absent, low-confidence, contradiction.

A gate approves only on a clear, confident "yes". Everything else --
silence, a "no", a hesitant yes, or a reply that says yes and no at
once -- leaves the gate unapproved, and require_approved_gate() refuses
to proceed. There is no bypass path: the only way through is an
approved gate object.
"""

import re

YES_WORDS = {"yes", "confirm", "approved", "go ahead", "go-ahead"}
NO_WORDS = {"no", "cancel", "stop", "reject", "do not"}
MIN_CONFIDENCE = 0.7


class GateResult:
    def __init__(self, status, reason):
        self.status = status
        self.reason = reason

    @property
    def approved(self):
        return self.status == "approved"

    def __repr__(self):
        return f"GateResult(status={self.status!r}, reason={self.reason!r})"


class ConfirmationGate:
    def __init__(self, action, min_confidence=MIN_CONFIDENCE):
        self.action = action
        self.min_confidence = min_confidence

    def evaluate(self, response, confidence=None):
        """Evaluate one reply. response=None/'' is the absent path."""
        if response is None or not str(response).strip():
            return GateResult("absent", "no reply received")
        text = str(response).strip().lower()
        has_yes = any(w in text for w in YES_WORDS)
        has_no = any(w in text for w in NO_WORDS)
        if has_yes and has_no:
            return GateResult("contradicting", "reply contains both approval and refusal")
        if has_no:
            return GateResult("rejected", "reply refuses the action")
        if not has_yes:
            return GateResult("unclear", "reply does not clearly approve")
        if confidence is None:
            return GateResult("low_confidence", "no confidence supplied")
        if confidence < self.min_confidence:
            return GateResult("low_confidence", f"confidence {confidence} below {self.min_confidence}")
        return GateResult("approved", "clear, confident approval")


def require_approved_gate(result, action=""):
    """Raise unless result is an approved gate result. This is the bypass guard."""
    if not isinstance(result, GateResult) or not result.approved:
        status = getattr(result, "status", "missing")
        raise PermissionError(f"gate not approved ({status}); action {action!r} refused")
    return True
