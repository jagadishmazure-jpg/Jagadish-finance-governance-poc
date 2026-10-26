import pytest
from finance_governance.cia import cia_review, CIAItem
from finance_governance.build_buy import build_vs_buy, Criterion
from finance_governance.evidence import classify_initiative, evidence_required

def _full_cia():
    return [CIAItem("confidentiality", "c1", True), CIAItem("integrity", "i1", True), CIAItem("availability", "a1", True)]

def test_cia_all_met_passes():
    r = cia_review(_full_cia())
    assert r["overall_pass"] is True and r["failed_legs"] == []

def test_cia_one_leg_fails_blocks_overall():
    items = _full_cia() + [CIAItem("availability", "a2", False)]
    r = cia_review(items)
    assert r["overall_pass"] is False and r["failed_legs"] == ["availability"]

def test_cia_empty_leg_scores_zero_and_fails():
    r = cia_review([CIAItem("confidentiality", "c1", True)])
    assert r["integrity"]["score"] == 0.0 and r["overall_pass"] is False

def test_cia_unknown_leg_rejected():
    with pytest.raises(ValueError):
        CIAItem("nope", "x", True)

def test_build_buy_weighted_winner():
    r = build_vs_buy([Criterion("control", 3, 9, 4), Criterion("speed", 2, 3, 9), Criterion("cost", 2, 7, 5)])
    assert r["recommendation"] == "build"
    assert r["build_total"] > r["buy_total"]

def test_build_buy_tie_evaluates_further():
    r = build_vs_buy([Criterion("only", 1, 5, 5)])
    assert r["recommendation"] == "evaluate_further"

def test_build_buy_negative_weight_rejected():
    with pytest.raises(ValueError):
        Criterion("w", -1, 5, 5)

def test_build_buy_score_out_of_range_rejected():
    with pytest.raises(ValueError):
        Criterion("w", 1, 11, 5)

def test_build_buy_empty_rejected():
    with pytest.raises(ValueError):
        build_vs_buy([])

def test_build_buy_weights_normalised():
    # Scaling all weights by 10 must not change the result.
    a = build_vs_buy([Criterion("x", 1, 9, 1), Criterion("y", 1, 1, 9)])
    b = build_vs_buy([Criterion("x", 10, 9, 1), Criterion("y", 10, 1, 9)])
    assert a["build_total"] == b["build_total"] and a["buy_total"] == b["buy_total"]

def test_evidence_production_claim_supported_when_full_evidence():
    r = classify_initiative("w", "production", ["live_usage_records", "incident_log", "audit_trail_sample", "performance_report"])
    assert r["awarded_grade"] == "production" and r["claim_supported"] is True

def test_evidence_production_claim_downgraded_when_evidence_missing():
    r = classify_initiative("w", "production", ["pilot_scope", "pilot_results", "known_limitations"])
    assert r["awarded_grade"] == "pilot" and r["claim_supported"] is False
    assert "live_usage_records" in r["missing_for_claim"]

def test_evidence_pilot_claim_downgraded_to_aspirational():
    r = classify_initiative("w", "pilot", ["concept_description"])
    assert r["awarded_grade"] == "aspirational"

def test_evidence_empty_set_is_ungraded():
    r = classify_initiative("w", "aspirational", [])
    assert r["awarded_grade"] == "ungraded" and r["missing_for_claim"] == ["concept_description"]

def test_evidence_required_lists_per_grade():
    assert evidence_required("production") == ["live_usage_records", "incident_log", "audit_trail_sample", "performance_report"]
    assert evidence_required("pilot") == ["pilot_scope", "pilot_results", "known_limitations"]
    assert evidence_required("aspirational") == ["concept_description"]

def test_evidence_unknown_grade_rejected():
    with pytest.raises(ValueError):
        evidence_required("mythical")
