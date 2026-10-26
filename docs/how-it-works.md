# How it works, step by step

1. Describe the idea. Give it a name and three pillar scores from 0
   to 100. Give it a grade claim and the evidence you actually hold.
2. Score it. `score_initiative` returns the mean, the weakest pillar,
   and a recommendation. If any pillar sits below 60, the
   recommendation is `blocked`, even if the other two are perfect.
3. Price it. Pick model options with per-thousand-token prices, then
   call `estimate_inference_cost` with token counts and query counts.
   `compare_models` sorts cheapest first. `budget_gate` checks the
   estimate against a budget. Any negative input raises an error.
4. Review security. Build a list of `CIAItem` rows, one per checklist
   item, marked met or not met. `cia_review` scores each leg. The
   overall verdict passes only when every leg is fully met.
5. Weigh build against buy. List criteria with weights and 0–10
   scores for each option. Weights are normalised, so scaling them
   cannot change the winner. A tie returns `evaluate_further`.
6. Grade the evidence. `classify_initiative` compares the evidence
   supplied with the evidence each grade needs, and awards the
   highest grade fully supported. A claim without its evidence is
   downgraded and the missing items are listed.
7. Gate the decision. A `ConfirmationGate` approves only a clear,
   confident yes. An `Approval` must name a person, name a scope,
   stay unexpired, and is spent on first use. `require_approved_gate`
   refuses any other path.
8. Read data safely. The store exposes one view,
   `v_initiative_scorecard`. Direct reads of the base table, reads of
   system tables, writes, and schema changes are denied by the
   authorizer. Fetches are capped with `fetchmany`.
9. Report cleanly. Run every free-text field through `redact_text`
   before it leaves the toolkit, so card numbers, email addresses,
   phone numbers, and SSNs never appear in outputs.
