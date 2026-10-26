"""8-word overlap check: repo docs/code vs a source text file.

Usage: python3 scripts/overlap_check.py <source-text-file>
Prints every shared 8-word window found in files under this repo
(excluding this script itself and .git). Exits 1 if any hit is found.
Normalisation: lowercase, ligatures expanded, punctuation removed.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def windows(text):
    text = text.lower().replace("\ufb01", "fi").replace("\ufb02", "fl")
    words = re.findall(r"[a-z0-9]+", text)
    return {" ".join(words[i:i + 8]) for i in range(len(words) - 7)}


def main():
    if len(sys.argv) != 2:
        print("usage: overlap_check.py <source-text-file>")
        return 2
    source_windows = windows(Path(sys.argv[1]).read_text(errors="ignore"))
    hits = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(ROOT))
        if rel.startswith((".git/", "scripts/overlap_check.py")) or "__pycache__" in rel:
            continue
        if path.suffix not in (".py", ".md", ".toml", ".txt"):
            continue
        for window in sorted(windows(path.read_text(errors="ignore")) & source_windows):
            hits.append((rel, window))
    for rel, window in hits:
        print(f"HIT {rel}: {window}")
    print(f"overlap hits: {len(hits)}")
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
