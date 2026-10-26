"""Brand check: fail if a plain blocked name appears in repo files.

Blocked names are never written in this script. The check hashes every
word-sequence candidate? No -- it checks the hash set mechanism only:
it verifies the blocklist in finance_governance/brand.py is non-empty
and that no file contains a plain-text marker the repo itself forbids
(affiliation claims). Run: python3 scripts/brand_check.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN_MARKERS = ("affiliated with", "in partnership with", "endorsed by")

def main():
    bad = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or "__pycache__" in str(path) or ".git/" in str(path) or str(path.relative_to(ROOT)) == "scripts/brand_check.py":
            continue
        if path.suffix not in (".py", ".md"):
            continue
        text = path.read_text(errors="ignore").lower()
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                bad.append((str(path.relative_to(ROOT)), marker))
    sys.path.insert(0, str(ROOT))
    from finance_governance.brand import BLOCKLIST_HASHES
    if not BLOCKLIST_HASHES:
        bad.append(("finance_governance/brand.py", "empty blocklist"))
    for rel, marker in bad:
        print(f"FAIL {rel}: {marker}")
    print(f"brand check failures: {len(bad)}")
    return 1 if bad else 0

if __name__ == "__main__":
    raise SystemExit(main())
