# Security policy

## Scope

This scaffold is a teaching and evaluation tool. It runs offline, uses
only the Python standard library, stores only synthetic rows in an
in-memory database, and has no network transport, no credentials, and
no real customer data.

## Reporting

If you find a weakness in a control claimed here, open an issue that
names the control and includes a failing test or a minimal reproduction.
Do not include real personal data, real credentials, or real customer
records in any report.

## Controls in place

- View-aware SQLite authorizer (see `docs/guardrails.md`).
- Confirmation gates and single-use, scoped, expiring approvals.
- PII redaction covering card numbers, email addresses, phone numbers,
  and SSNs.
- Row caps enforced at fetch time.
- Negative cost and budget inputs rejected.
- Email channel dry-run by default and refused in CI.
- Brand blocklist stored as hashes, never as plain names.

## What this is not

This is not a compliance certification, not legal advice, and not a
production governance system. A real deployment needs review by the
owning firm's risk, legal, and security teams.
