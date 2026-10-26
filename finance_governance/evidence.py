"""Production / pilot / aspirational grading by evidence, not by claim.

A vendor or team claim is graded only against the evidence actually
supplied. Each grade names the evidence it requires; supplying less
downgrades the grade. Nothing is upgraded on the strength of a claim
alone.
"""

EVIDENCE_REQUIRED = {
    "production": [
        "live_usage_records",
        "incident_log",
        "audit_trail_sample",
        "performance_report",
    ],
    "pilot": [
        "pilot_scope",
        "pilot_results",
        "known_limitations",
    ],
    "aspirational": [
        "concept_description",
    ],
}

GRADES = ("production", "pilot", "aspirational")


def evidence_required(grade):
    if grade not in EVIDENCE_REQUIRED:
        raise ValueError(f"unknown grade: {grade!r}")
    return list(EVIDENCE_REQUIRED[grade])


def classify_initiative(name, claimed_grade, evidence):
    """Grade an initiative from its evidence set.

    claimed_grade is recorded but never trusted: the returned grade is
    the highest grade whose full evidence set is present. Missing
    evidence for the claimed grade downgrades, step by step.
    """
    if claimed_grade not in GRADES:
        raise ValueError(f"unknown claimed grade: {claimed_grade!r}")
    supplied = set(evidence)
    for grade in ("production", "pilot", "aspirational"):
        if set(EVIDENCE_REQUIRED[grade]).issubset(supplied):
            awarded = grade
            break
    else:  # pragma: no cover - aspirational needs one item; empty set reaches here
        awarded = "ungraded"
    missing_for_claim = [e for e in EVIDENCE_REQUIRED[claimed_grade] if e not in supplied]
    return {
        "name": name,
        "claimed_grade": claimed_grade,
        "awarded_grade": awarded,
        "claim_supported": awarded == claimed_grade,
        "missing_for_claim": missing_for_claim,
    }
