"""Named-person, single-use, scoped, expiring approvals."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


class ApprovalError(Exception):
    pass


@dataclass
class Approval:
    approver: str
    scope: str
    expires_at: datetime
    _used: bool = field(default=False, init=False)

    def __post_init__(self):
        if not self.approver or not self.approver.strip():
            raise ApprovalError("approver must be a named person")
        if not self.scope or not self.scope.strip():
            raise ApprovalError("scope must be non-empty")
        if self.expires_at.tzinfo is None:
            raise ApprovalError("expires_at must carry a timezone")

    @classmethod
    def create(cls, approver, scope, minutes_valid=60):
        if minutes_valid <= 0:
            raise ApprovalError("minutes_valid must be positive")
        return cls(approver=approver, scope=scope,
                   expires_at=datetime.now(timezone.utc) + timedelta(minutes=minutes_valid))

    def consume(self, scope, now=None):
        """Consume the approval for one action. Second use always fails."""
        now = now or datetime.now(timezone.utc)
        if self._used:
            raise ApprovalError("approval already used")
        if now >= self.expires_at:
            raise ApprovalError("approval expired")
        if scope != self.scope:
            raise ApprovalError("approval scope mismatch")
        self._used = True
        return True
