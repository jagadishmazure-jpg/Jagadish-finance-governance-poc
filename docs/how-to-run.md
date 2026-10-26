# How to run (offline first)

Requirements: Python 3.10 or newer, system `pytest`. No third-party
packages, no network, no accounts, no keys.

```bash
cd Jagadish-finance-governance-poc
python3 -m pytest tests -q
PYTHONPATH=. python3 -m finance_governance.demo
PYTHONPATH=. python3 examples/worked_example.py
```

There is no cloud step and no optional cloud step: this scaffold is
offline by design. Do not create a virtual environment inside this
directory.
