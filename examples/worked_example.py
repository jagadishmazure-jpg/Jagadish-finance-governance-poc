"""Runnable worked example: prints the full governance packet."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from finance_governance.demo import main

if __name__ == "__main__":
    main()
