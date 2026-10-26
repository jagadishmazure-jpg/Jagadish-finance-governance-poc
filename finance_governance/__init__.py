"""Finance governance proof-of-concept toolkit (standard library only).

All data handled here is synthetic. Nothing in this package talks to a
real bank, a real vendor, or a live model service.
"""

from .scorecard import Scorecard, score_initiative
from .economics import ModelOption, estimate_inference_cost, compare_models, budget_gate
from .cia import cia_review, CIAItem
from .build_buy import build_vs_buy, Criterion
from .evidence import classify_initiative, evidence_required, GRADES
from .approvals import Approval, ApprovalError
from .gates import ConfirmationGate, GateResult, require_approved_gate
from .pii import redact_text, PII_CHECKLIST
from .store import create_governed_connection, fetch_capped, RowCapExceeded
from .notify import EmailChannel, EmailRefused
from .brand import BLOCKLIST_HASHES, is_blocked_hash

__all__ = [
    "Scorecard", "score_initiative", "ModelOption", "estimate_inference_cost",
    "compare_models", "budget_gate", "cia_review", "CIAItem",
    "build_vs_buy", "Criterion", "GRADES", "classify_initiative",
    "evidence_required", "Approval", "ApprovalError", "ConfirmationGate",
    "GateResult", "require_approved_gate", "redact_text", "PII_CHECKLIST",
    "create_governed_connection", "fetch_capped", "RowCapExceeded",
    "EmailChannel", "EmailRefused", "BLOCKLIST_HASHES", "is_blocked_hash",
]
