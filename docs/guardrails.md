# Guardrails and security controls

| Control | How it is enforced | Proof test |
| --- | --- | --- |
| View-aware SQLite authorizer | Base-table reads need an allowed view as source; system tables, writes, PRAGMA, ATTACH, and schema changes denied | `test_authorizer_denies_direct_base_table_read`, `test_authorizer_denies_sqlite_master_read`, `test_authorizer_denies_write`, `test_authorizer_denies_update_and_delete`, `test_authorizer_denies_pragma`, `test_authorizer_denies_attach`, `test_authorizer_denies_schema_change`, `test_authorizer_denies_direct_rowid_read` |
| Authorizer test style | Tests assert the exception type only, never error wording | All authorizer tests above |
| Confirmation gate | Only a clear, confident yes approves | `test_gate_approved_on_clear_confident_yes` |
| Gate bypass | `require_approved_gate` refuses non-gate and unapproved values | `test_gate_bypass_refused_without_gate_result` |
| Gate reject / absent | "no" rejects; missing reply is absent | `test_gate_reject_path_blocks`, `test_gate_absent_path_blocks` |
| Gate low confidence | Confidence below 0.7, or none supplied, blocks | `test_gate_low_confidence_blocks`, `test_gate_confidence_boundary` |
| Gate contradiction | A reply holding yes and no together blocks | `test_gate_self_contradicting_consent_blocks` |
| Approvals | Named person, single use, scoped, expiring | `test_approval_named_person_required`, `test_approval_single_use`, `test_approval_scoped`, `test_approval_expiring` |
| PII redaction | Card, email, phone, SSN patterns replaced | `test_pii_card_number_redacted`, `test_pii_email_redacted`, `test_pii_phone_and_ssn_redacted`, `test_pii_checklist_includes_cards_and_emails` |
| Row cap | `fetchmany(MAX+1)`; over-cap raises, never silently truncates | `test_row_cap_exceeded_raises`, `test_row_cap_exact_limit_passes` |
| Negative cost rejection | Every cost input checked before arithmetic | `test_negative_input_tokens_rejected`, `test_negative_output_tokens_rejected`, `test_negative_queries_rejected`, `test_negative_price_rejected`, `test_budget_gate_negative_estimate_rejected` |
| Brand blocklist | Stored as hashes; non-empty asserted | `test_brand_blocklist_non_empty`, `test_brand_hash_lookup_blocks_known_digest` |
| Email safety | Dry-run default; opt-in required; refused in CI | `test_email_dry_run_by_default`, `test_email_no_opt_in_no_send_even_when_not_dry_run`, `test_email_refused_in_ci` |
| Fail-closed scorecard | Any pillar below threshold blocks | `test_fail_closed_one_pillar_below_threshold_blocks`, `test_fail_closed_each_pillar_can_block` |
| Evidence grades | Award follows evidence, not the claim | `test_evidence_production_claim_downgraded_when_evidence_missing` |

No credentials live in this repo. The email channel has no transport
wired in; an opt-in send is recorded as a would-send, not delivered.
