"""CIA-triad security review as a scored checklist.

Each leg -- confidentiality, integrity, availability -- holds checklist
items. An item is either met or not met; there is no partial credit in
the stored result, so a reviewer cannot smuggle a half-answer into a
pass. A leg with no items scores 0 and fails, never passes by default.
"""

from dataclasses import dataclass

LEGS = ("confidentiality", "integrity", "availability")


@dataclass(frozen=True)
class CIAItem:
    leg: str
    check: str
    met: bool

    def __post_init__(self):
        if self.leg not in LEGS:
            raise ValueError(f"unknown leg: {self.leg!r}")
        if not isinstance(self.met, bool):
            raise TypeError("met must be a bool")


def cia_review(items):
    """Score each leg and the whole review.

    Returns a dict with per-leg met/total/score and an overall verdict.
    Overall is "pass" only when every leg scores 100 percent.
    """
    out = {}
    for leg in LEGS:
        leg_items = [i for i in items if i.leg == leg]
        met = sum(1 for i in leg_items if i.met)
        total = len(leg_items)
        score = round(100.0 * met / total, 2) if total else 0.0
        out[leg] = {"met": met, "total": total, "score": score, "pass": total > 0 and met == total}
    out["overall_pass"] = all(out[leg]["pass"] for leg in LEGS)
    out["failed_legs"] = [leg for leg in LEGS if not out[leg]["pass"]]
    return out
