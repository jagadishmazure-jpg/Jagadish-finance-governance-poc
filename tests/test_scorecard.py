import pytest
from finance_governance.scorecard import score_initiative, Scorecard

def test_all_pillars_pass_gives_deploy_candidate():
    c = score_initiative("a", {"risk": 80, "explainability": 75, "auditability": 90})
    assert c.recommendation == "deploy_candidate"
    assert c.mean_score == 81.67

def test_fail_closed_one_pillar_below_threshold_blocks():
    c = score_initiative("b", {"risk": 80, "explainability": 59.9, "auditability": 90})
    assert c.recommendation == "blocked"
    assert c.blocked_pillars == ["explainability"]

def test_fail_closed_each_pillar_can_block():
    for pillar in ("risk", "explainability", "auditability"):
        scores = {"risk": 90, "explainability": 90, "auditability": 90}
        scores[pillar] = 10
        assert score_initiative("x", scores).recommendation == "blocked"

def test_fail_closed_threshold_boundary_passes_at_threshold():
    c = score_initiative("c", {"risk": 60, "explainability": 60, "auditability": 60})
    assert c.recommendation == "deploy_candidate"

def test_missing_pillar_raises_never_passes():
    with pytest.raises(ValueError):
        score_initiative("d", {"risk": 80, "explainability": 75})

def test_out_of_range_score_raises():
    with pytest.raises(ValueError):
        score_initiative("e", {"risk": 101, "explainability": 75, "auditability": 90})

def test_weakest_pillar_named():
    c = score_initiative("f", {"risk": 70, "explainability": 95, "auditability": 80})
    assert c.weakest == "risk"
