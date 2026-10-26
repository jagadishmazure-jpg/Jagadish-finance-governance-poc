"""Build-versus-buy decision with weighted criteria.

Weights are normalised, so a caller cannot inflate one criterion by
scaling all weights. Scores are 0-10 per option per criterion. Negative
weights, negative scores, and scores above 10 raise.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Criterion:
    name: str
    weight: float
    build_score: float
    buy_score: float

    def __post_init__(self):
        if self.weight < 0:
            raise ValueError("weight must not be negative")
        for label, value in (("build_score", self.build_score), ("buy_score", self.buy_score)):
            if not 0 <= value <= 10:
                raise ValueError(f"{label} must be between 0 and 10")


def build_vs_buy(criteria):
    """Return normalised weighted totals and a recommendation.

    Ties recommend "evaluate_further", never a coin-flip winner.
    """
    if not criteria:
        raise ValueError("at least one criterion is required")
    total_weight = sum(c.weight for c in criteria)
    if total_weight <= 0:
        raise ValueError("total weight must be positive")
    build_total = round(sum(c.weight / total_weight * c.build_score for c in criteria), 4)
    buy_total = round(sum(c.weight / total_weight * c.buy_score for c in criteria), 4)
    if build_total > buy_total:
        recommendation = "build"
    elif buy_total > build_total:
        recommendation = "buy"
    else:
        recommendation = "evaluate_further"
    return {
        "build_total": build_total,
        "buy_total": buy_total,
        "recommendation": recommendation,
        "criteria": [
            {"name": c.name, "normalised_weight": round(c.weight / total_weight, 4),
             "build_score": c.build_score, "buy_score": c.buy_score}
            for c in criteria
        ],
    }
