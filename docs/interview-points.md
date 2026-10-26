# Interview points

- Fail-closed beats averaging: a single weak pillar blocks deployment
  even when the mean looks strong. I can show the test where a 59.9
  pillar blocks a 90/90 companion pair.
- Evidence grading separates claims from proof: a production claim
  with only trial evidence is downgraded, and the missing items are
  named. That is the check I would run on any vendor statement.
- The authorizer is view-aware, not table-aware: base tables are
  readable only when the authorizer's source names an allowed view.
  Direct reads, system-table reads, writes, and schema changes are
  denied, and tests assert denial by exception type, not by message
  wording.
- The row cap is enforced at fetch time with `fetchmany(MAX+1)`,
  deliberately without rewriting the query or calling `fetchall`,
  so over-cap results surface as errors instead of silent pages.
- Gates are tested on five paths, not one: approve, bypass attempt,
  reject, absent, low confidence, and self-contradicting consent.
  The last two are the paths most gate designs forget.
- PII redaction failed in earlier portfolio work when checklists
  named only phone and SSN. This repo's checklist names card numbers
  and email addresses explicitly, with a test for each.
- Everything is synthetic and offline: the firm is invented, the
  prices are invented, and the suite needs no network or keys.
