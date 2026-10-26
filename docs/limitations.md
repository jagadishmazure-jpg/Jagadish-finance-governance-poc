# Limitations and known failures

- Scores are reviewer judgements, not measurements. Two reviewers can
  score the same idea differently; the toolkit makes the disagreement
  visible, it does not resolve it.
- Cost estimates use caller-supplied prices and token counts. If those
  inputs are wrong, the estimate is wrong in the same direction.
- The evidence grader checks that named evidence items are present in
  a list. It does not open, read, or verify the underlying documents.
- The CIA checklist is binary per item. Real reviews often need
  partial credit and compensating controls; those are out of scope
  here and are recorded as a planned extension, not a present feature.
- The SQLite store is in-memory and synthetic. It is a control demo,
  not a system of record.
- Known failure kept visible as a test: a query returning more rows
  than the cap raises `RowCapExceeded` instead of returning a partial
  page (`test_row_cap_exceeded_raises`). Callers must handle that
  error; silent truncation was rejected as a design choice.
- The email channel never delivers mail in this scaffold, even with
  opt-in. That is deliberate: delivery needs a reviewed transport and
  credentials outside this repo.
