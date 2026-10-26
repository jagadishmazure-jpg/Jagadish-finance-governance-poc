import pytest
from datetime import datetime, timedelta, timezone
from finance_governance.gates import ConfirmationGate, GateResult, require_approved_gate
from finance_governance.approvals import Approval, ApprovalError

GATE = ConfirmationGate("deploy")

def test_gate_approved_on_clear_confident_yes():
    r = GATE.evaluate("yes", confidence=0.9)
    assert r.approved is True and r.status == "approved"

def test_gate_bypass_refused_without_gate_result():
    with pytest.raises(PermissionError):
        require_approved_gate(None, "deploy")
    with pytest.raises(PermissionError):
        require_approved_gate("yes", "deploy")

def test_gate_reject_path_blocks():
    r = GATE.evaluate("no", confidence=0.9)
    assert r.status == "rejected" and not r.approved
    with pytest.raises(PermissionError):
        require_approved_gate(r, "deploy")

def test_gate_absent_path_blocks():
    for reply in (None, "", "   "):
        r = GATE.evaluate(reply, confidence=0.9)
        assert r.status == "absent" and not r.approved
        with pytest.raises(PermissionError):
            require_approved_gate(r, "deploy")

def test_gate_low_confidence_blocks():
    r = GATE.evaluate("yes", confidence=0.3)
    assert r.status == "low_confidence" and not r.approved
    r2 = GATE.evaluate("yes", confidence=None)
    assert r2.status == "low_confidence"

def test_gate_self_contradicting_consent_blocks():
    for reply in ("yes, wait, no", "yes but no", "confirm, actually no"):
        r = GATE.evaluate(reply, confidence=0.95)
        assert r.status == "contradicting", reply
        assert not r.approved

def test_gate_unclear_reply_blocks():
    r = GATE.evaluate("maybe later", confidence=0.95)
    assert r.status == "unclear" and not r.approved

def test_gate_confidence_boundary():
    assert GATE.evaluate("yes", confidence=0.7).approved is True
    assert GATE.evaluate("yes", confidence=0.69).approved is False

def test_approval_named_person_required():
    with pytest.raises(ApprovalError):
        Approval(approver="  ", scope="deploy", expires_at=datetime.now(timezone.utc) + timedelta(hours=1))

def test_approval_single_use():
    ap = Approval.create("Priya Nair", "deploy invoice-helper")
    assert ap.consume("deploy invoice-helper") is True
    with pytest.raises(ApprovalError):
        ap.consume("deploy invoice-helper")

def test_approval_scoped():
    ap = Approval.create("Priya Nair", "deploy invoice-helper")
    with pytest.raises(ApprovalError):
        ap.consume("deploy memo-drafter")

def test_approval_expiring():
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    ap = Approval(approver="Priya Nair", scope="deploy", expires_at=past)
    with pytest.raises(ApprovalError):
        ap.consume("deploy")
