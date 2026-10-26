"""Governance scorecard: three pillars, fail-closed.

Scores are 0-100 per pillar. A missing pillar is not treated as zero
silently and it is not treated as a pass: it blocks the recommendation.
The same holds for any pillar below the threshold. There is no path
that turns a weak pillar into a deploy recommendation.
"""

from dataclasses import dataclass, field

THRESHOLD = 60.0
PILLARS = ("risk", "explainability", "auditability")


def _check_score(name, value):
    if value is None:
        raise ValueError(f"pillar {name!r} is missing")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"pillar {name!r} must be a number")
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError(f"pillar {name!r} must be finite")
    if not 0 <= value <= 100:
        raise ValueError(f"pillar {name!r} must be between 0 and 100")
    return float(value)


@dataclass(frozen=True)
class Scorecard:
    """One initiative scored on the three pillars."""

    name: str
    risk: float
    explainability: float
    auditability: float
    threshold: float = THRESHOLD

    def __post_init__(self):
        for pillar in PILLARS:
            _check_score(pillar, getattr(self, pillar))
        if not 0 < self.threshold <= 100:
            raise ValueError("threshold must be between 0 (exclusive) and 100")

    @property
    def pillars(self):
        return {p: getattr(self, p) for p in PILLARS}

    @property
    def weakest(self):
        return min(self.pillars, key=self.pillars.get)

    @property
    def blocked_pillars(self):
        return [p for p in PILLARS if self.pillars[p] < self.threshold]

    @property
    def recommendation(self):
        # Fail-closed: any pillar below threshold blocks deployment.
        return "blocked" if self.blocked_pillars else "deploy_candidate"

    @property
    def mean_score(self):
        return round(sum(self.pillars.values()) / len(PILLARS), 2)


def score_initiative(name, scores, threshold=THRESHOLD):
    """Build a Scorecard from a mapping. Missing pillars raise, never pass.

    >>> score_initiative("demo", {"risk": 80, "explainability": 75, "auditability": 90}).recommendation
    'deploy_candidate'
    >>> score_initiative("demo", {"risk": 80, "explainability": 40, "auditability": 90}).recommendation
    'blocked'
    """
    missing = [p for p in PILLARS if p not in scores]
    if missing:
        raise ValueError(f"missing pillars: {missing}")
    return Scorecard(name=name, threshold=threshold, **{p: scores[p] for p in PILLARS})
