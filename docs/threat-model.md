# Threat model

## Assets

- Reviewer judgements (pillar scores, evidence lists).
- Synthetic initiative rows in the in-memory store.
- Approval records and gate outcomes.

## Threats (STRIDE, applied narrowly)

- Spoofing: an unnamed or borrowed approval lets someone else's
  decision pass. Mitigation: approvals require a named person.
- Tampering: a query writes or alters scores after review.
  Mitigation: authorizer denies writes and schema changes.
- Repudiation: a decision cannot be traced to a person or scope.
  Mitigation: approvals are scoped, expiring, and single-use.
- Information disclosure: base tables or system tables leak notes
  the view hides; logs leak card or email data. Mitigation:
  view-only reads, redaction before output.
- Denial of service: an unbounded fetch exhausts memory.
  Mitigation: fetch-time row cap that raises over the limit.
- Elevation of privilege: a gate is bypassed, or a hesitant or
  contradictory reply is read as consent. Mitigation: only an
  approved gate object passes `require_approved_gate`; low
  confidence and contradiction both block.

## Out of scope

Model prompt attacks, model output attacks, and network attacks are
out of scope: this scaffold runs no model and makes no network calls.
A production version would need those reviews separately.

## ADRs

### ADR-1: Fail-closed scoring

Decision: any pillar below threshold blocks deployment.
Alternatives considered: averaging pillars; blocking only on the
mean. Rejected because a strong average can hide a fatal weakness in
one pillar, which is exactly the case a governance review exists to
catch.

### ADR-2: View-only data access

Decision: reporting queries read one view; the authorizer denies
base-table reads unless the view is the source.
Alternatives considered: read-only connection alone. Rejected
because a read-only connection still exposes every column, including
reviewer notes the view hides.

### ADR-3: Fetch-time row cap

Decision: cap with `fetchmany(MAX+1)` and raise over the cap.
Alternatives considered: rewriting queries with a limit clause;
silently returning the first page. Rejected because rewriting
changes reviewer queries, and silent paging hides missing rows.

### ADR-4: Evidence follows the artefact list, not the claim

Decision: the awarded grade is the highest grade whose evidence set
is fully present.
Alternatives considered: trusting the claimed grade with a warning.
Rejected because a warning is easy to ignore and the downgrade with
named missing items is the useful output.

### ADR-5: Standard library only, offline

Decision: no third-party packages, no network, no credentials.
Alternatives considered: a web framework and a hosted database.
Rejected for a scaffold whose point is review logic: dependencies
and hosting would add risk without adding a review capability.
