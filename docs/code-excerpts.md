# Real code excerpts and their real output

Excerpt — fail-closed scoring (`finance_governance/scorecard.py`):

```python
@property
def recommendation(self):
    # Fail-closed: any pillar below threshold blocks deployment.
    return "blocked" if self.blocked_pillars else "deploy_candidate"
```

Excerpt — negative inputs rejected (`finance_governance/economics.py`):

```python
if value < 0:
    raise ValueError(f"{name} must not be negative")
```

Excerpt — the gate's only approval path (`finance_governance/gates.py`):

```python
def require_approved_gate(result, action=""):
    if not isinstance(result, GateResult) or not result.approved:
        raise PermissionError(f"gate not approved; action {action!r} refused")
    return True
```

Real output — `PYTHONPATH=. python3 -m finance_governance.demo`:

```
scorecard invoice-helper mean=81.67 recommendation=deploy_candidate
scorecard memo-drafter weakest=risk blocked=['risk'] recommendation=blocked
cost comparison (1000 in / 500 out x 10): [{'model': 'small', 'estimate': 0.02}, {'model': 'large', 'estimate': 0.25}]
budget gate 0.20 vs 100.0: True
CIA overall_pass=False failed_legs=['availability']
build-vs-buy: build
evidence: {'name': 'risk-watcher', 'claimed_grade': 'production', 'awarded_grade': 'production', 'claim_supported': True, 'missing_for_claim': []}
redacted: contact [REDACTED:EMAIL] or card [REDACTED:CARD]
```

The worked example is synthetic: the firm, the initiatives, the
prices, and the scores are invented to exercise the code.
