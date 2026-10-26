"""Worked synthetic example for Fernwick Bank (fictional firm).

Run:  python3 -m finance_governance.demo
"""

from .scorecard import score_initiative
from .economics import ModelOption, compare_models, budget_gate
from .cia import cia_review, CIAItem
from .build_buy import build_vs_buy, Criterion
from .evidence import classify_initiative
from .pii import redact_text


def main():
    card = score_initiative("invoice-helper", {"risk": 80, "explainability": 75, "auditability": 90})
    print(f"scorecard invoice-helper mean={card.mean_score} recommendation={card.recommendation}")
    weak = score_initiative("memo-drafter", {"risk": 55, "explainability": 82, "auditability": 88})
    print(f"scorecard memo-drafter weakest={weak.weakest} blocked={weak.blocked_pillars} recommendation={weak.recommendation}")
    options = [ModelOption("small", 0.001, 0.002), ModelOption("large", 0.01, 0.03)]
    print(f"cost comparison (1000 in / 500 out x 10): {compare_models(options, 1000, 500, queries=10)}")
    print(f"budget gate 0.20 vs 100.0: {budget_gate(0.20, 100.0)}")
    review = cia_review([
        CIAItem("confidentiality", "access limited to reviewers", True),
        CIAItem("integrity", "outputs logged immutably", True),
        CIAItem("availability", "fallback to manual review", False),
    ])
    print(f"CIA overall_pass={review['overall_pass']} failed_legs={review['failed_legs']}")
    print(f"build-vs-buy: {build_vs_buy([Criterion('control', 3, 9, 4), Criterion('speed', 2, 3, 9), Criterion('cost', 2, 7, 5)])['recommendation']}")
    print(f"evidence: {classify_initiative('risk-watcher', 'production', ['live_usage_records', 'incident_log', 'audit_trail_sample', 'performance_report'])}")
    print(f"redacted: {redact_text('contact ana@example.test or card 4111 1111 1111 1111')}")


if __name__ == "__main__":
    main()
