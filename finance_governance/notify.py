"""Email channel: dry-run by default, explicit opt-in to send.

No credentials are stored in this repo and none are read here. Sending
is refused outright when a CI environment marker is present, because a
demo must never become a real send from an automated run.
"""

import os


class EmailRefused(Exception):
    pass


class EmailChannel:
    def __init__(self, dry_run=True):
        self.dry_run = dry_run

    def send(self, to, subject, body, explicit_opt_in=False):
        if os.environ.get("CI", "").lower() in ("true", "1"):
            raise EmailRefused("refused: CI environment")
        if self.dry_run and not explicit_opt_in:
            return {"sent": False, "dry_run": True, "to": to, "subject": subject}
        if not explicit_opt_in:
            raise EmailRefused("refused: sending needs explicit opt-in")
        # No real transport is wired in this scaffold; an opt-in send is
        # recorded as a would-send so callers can see the decision point.
        return {"sent": False, "dry_run": False, "would_send": True, "to": to, "subject": subject}
