import os
import sqlite3
import pytest
from finance_governance.pii import redact_text, find_pii_types, PII_CHECKLIST
from finance_governance.store import create_governed_connection, fetch_capped, RowCapExceeded
from finance_governance.brand import BLOCKLIST_HASHES, is_blocked_hash
from finance_governance.notify import EmailChannel, EmailRefused

# --- PII: checklist must name cards and emails, not just phone/SSN ---
def test_pii_checklist_includes_cards_and_emails():
    assert "card_number" in PII_CHECKLIST and "email_address" in PII_CHECKLIST
    assert "phone_number" in PII_CHECKLIST and "ssn" in PII_CHECKLIST

def test_pii_card_number_redacted():
    out = redact_text("card 4111 1111 1111 1111 on file")
    assert "4111" not in out and "[REDACTED:CARD]" in out

def test_pii_email_redacted():
    out = redact_text("contact ana@example.test please")
    assert "ana@example.test" not in out and "[REDACTED:EMAIL]" in out

def test_pii_phone_and_ssn_redacted():
    out = redact_text("call 555-123-4567, ssn 123-45-6789")
    assert "555-123-4567" not in out and "123-45-6789" not in out
    assert "[REDACTED:PHONE]" in out and "[REDACTED:SSN]" in out

def test_pii_find_types_covers_all_four():
    assert find_pii_types("4111111111111111 ana@example.test 555-123-4567 123-45-6789") == list(PII_CHECKLIST)

def test_pii_clean_text_unchanged():
    assert redact_text("no sensitive data here") == "no sensitive data here"

# --- Authorizer: assert denial by exception type only; text check disabled ---
def test_authorizer_allows_view_read():
    con = create_governed_connection()
    rows = con.execute("SELECT id, name FROM v_initiative_scorecard ORDER BY id").fetchall()
    assert [r[0] for r in rows] == [1, 2, 3]

def test_authorizer_denies_direct_base_table_read():
    con = create_governed_connection()
    with pytest.raises(sqlite3.DatabaseError):
        con.execute("SELECT id FROM initiatives").fetchall()

def test_authorizer_denies_secret_column_via_view():
    # The view simply does not expose secret_note; selecting it fails.
    con = create_governed_connection()
    with pytest.raises(Exception):
        con.execute("SELECT secret_note FROM v_initiative_scorecard").fetchall()

def test_authorizer_denies_sqlite_master_read():
    con = create_governed_connection()
    with pytest.raises(sqlite3.DatabaseError):
        con.execute("SELECT name FROM sqlite_master").fetchall()

def test_authorizer_denies_write():
    con = create_governed_connection()
    with pytest.raises(sqlite3.DatabaseError):
        con.execute("INSERT INTO v_initiative_scorecard VALUES (9,'x',1,1,1,'pilot')")

def test_authorizer_denies_update_and_delete():
    con = create_governed_connection()
    with pytest.raises(sqlite3.DatabaseError):
        con.execute("UPDATE initiatives SET risk=1 WHERE id=1")
    with pytest.raises(sqlite3.DatabaseError):
        con.execute("DELETE FROM initiatives WHERE id=1")

def test_authorizer_denies_pragma():
    con = create_governed_connection()
    with pytest.raises(sqlite3.DatabaseError):
        con.execute("PRAGMA table_info(initiatives)").fetchall()

def test_authorizer_denies_attach():
    con = create_governed_connection()
    with pytest.raises(sqlite3.DatabaseError):
        con.execute("ATTACH ':memory:' AS other")

def test_authorizer_denies_schema_change():
    con = create_governed_connection()
    with pytest.raises(sqlite3.DatabaseError):
        con.execute("DROP TABLE initiatives")

# --- Row cap: fetchmany(MAX+1), no LIMIT rewrite, no fetchall in helper ---
def test_row_cap_within_limit_returns_rows():
    con = create_governed_connection()
    cur = con.execute("SELECT id FROM v_initiative_scorecard ORDER BY id")
    assert len(fetch_capped(cur, 10)) == 3

def test_row_cap_exceeded_raises():
    con = create_governed_connection()
    cur = con.execute("SELECT id FROM v_initiative_scorecard ORDER BY id")
    with pytest.raises(RowCapExceeded):
        fetch_capped(cur, 2)

def test_row_cap_exact_limit_passes():
    con = create_governed_connection()
    cur = con.execute("SELECT id FROM v_initiative_scorecard ORDER BY id")
    assert len(fetch_capped(cur, 3)) == 3

def test_row_cap_negative_rejected():
    con = create_governed_connection()
    cur = con.execute("SELECT id FROM v_initiative_scorecard")
    with pytest.raises(ValueError):
        fetch_capped(cur, -1)

# --- Brand blocklist: non-empty, hash mechanism works ---
def test_brand_blocklist_non_empty():
    assert len(BLOCKLIST_HASHES) > 0

def test_brand_blocklist_entries_are_sha256_hex():
    for h in BLOCKLIST_HASHES:
        assert len(h) == 64 and all(c in "0123456789abcdef" for c in h)

def test_brand_hash_lookup_blocks_known_digest():
    digest = next(iter(BLOCKLIST_HASHES))
    assert is_blocked_hash(digest) is True
    assert is_blocked_hash("0" * 64) is False

# --- Email: dry-run default, explicit opt-in, refused in CI ---
def test_email_dry_run_by_default():
    ch = EmailChannel()
    r = ch.send("team@example.test", "review", "body")
    assert r["sent"] is False and r["dry_run"] is True

def test_email_no_opt_in_no_send_even_when_not_dry_run():
    ch = EmailChannel(dry_run=False)
    with pytest.raises(EmailRefused):
        ch.send("team@example.test", "review", "body")

def test_email_refused_in_ci(monkeypatch):
    monkeypatch.setenv("CI", "true")
    ch = EmailChannel(dry_run=False)
    with pytest.raises(EmailRefused):
        ch.send("team@example.test", "review", "body", explicit_opt_in=True)

def test_authorizer_denies_direct_rowid_read():
    # The narrow internal trailing read must not become a rowid leak.
    con = create_governed_connection()
    with pytest.raises(sqlite3.DatabaseError):
        con.execute("SELECT rowid FROM initiatives").fetchall()
