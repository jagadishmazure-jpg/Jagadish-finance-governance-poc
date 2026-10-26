"""Trial pricing: picking a model and estimating call spend.

Every money or quantity input is checked for negativity before any
arithmetic happens. A negative input is a caller error, not a discount:
it raises ValueError and no estimate is returned.
"""

from dataclasses import dataclass


def _non_negative(name, value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number")
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError(f"{name} must be finite")
    if value < 0:
        raise ValueError(f"{name} must not be negative")
    return float(value)


@dataclass(frozen=True)
class ModelOption:
    name: str
    price_per_1k_input: float
    price_per_1k_output: float
    fixed_monthly: float = 0.0

    def __post_init__(self):
        for field_name in ("price_per_1k_input", "price_per_1k_output", "fixed_monthly"):
            _non_negative(field_name, getattr(self, field_name))


def estimate_inference_cost(option, input_tokens, output_tokens, queries=1):
    """Estimate cost for a batch of queries. No input may be negative.

    >>> opt = ModelOption("small", 0.001, 0.002)
    >>> estimate_inference_cost(opt, 1000, 500, queries=10)
    0.02
    """
    n_in = _non_negative("input_tokens", input_tokens)
    n_out = _non_negative("output_tokens", output_tokens)
    n_q = _non_negative("queries", queries)
    per_query = (n_in / 1000.0) * option.price_per_1k_input + (n_out / 1000.0) * option.price_per_1k_output
    return round(per_query * n_q + option.fixed_monthly, 6)


def compare_models(options, input_tokens, output_tokens, queries=1):
    """Return options sorted cheapest-first, each with its estimate."""
    rows = [
        {"model": opt.name, "estimate": estimate_inference_cost(opt, input_tokens, output_tokens, queries)}
        for opt in options
    ]
    return sorted(rows, key=lambda r: r["estimate"])


def budget_gate(estimate, budget):
    """True only when the estimate fits the budget. Negatives raise.

    >>> budget_gate(50.0, 100.0)
    True
    >>> budget_gate(150.0, 100.0)
    False
    """
    est = _non_negative("estimate", estimate)
    bud = _non_negative("budget", budget)
    return est <= bud
