# Knowledge notes — distilled patterns (own words)

These notes distil the patterns this repo implements. They are written
fresh from the concepts, not copied from any source document.

## Pattern 1: Judge before you launch

A finance idea should pass a structured review before it reaches
users. The review looks at how risky the idea is, how clearly its
reasoning can be shown, and how completely its actions can be traced
afterwards. A weakness in any one of those areas stops the launch,
even when the other two look strong.

## Pattern 2: Price the trial honestly

A trial has two price questions: which model to run, and what each
call costs at the volumes the trial will actually use. Compare options
on the same token counts and query counts, then check the cheapest
honest option against the budget. Reject any input that is negative:
a negative price or count is a data error, not a saving.

## Pattern 3: Check secrecy, correctness, uptime separately

Security review is clearer as three separate lists: who can see the
data, whether outputs stay correct and tamper-evident, and whether
the service stays available with a manual fallback. A pass needs all
three lists fully met; a single failed leg fails the review.

## Pattern 4: Build or buy on stated weights

Choosing between building and buying works only when the criteria
and their weights are written down first. Normalise the weights so
their scale cannot tilt the answer, score both options on the same
criteria, and treat a tie as "look closer", not as a winner.

## Pattern 5: Grade claims by evidence

Ideas sit at different stages: running live with real users, running
as a bounded trial, or still an idea. Each stage needs its own
evidence. A live claim needs live records, incident history, sample
trails, and performance reports. A trial claim needs its scope, its
results, and its known limits. An idea needs only a description — and
must be labelled as an idea, not as a live system.

## Pattern 6: Trust is a change process

People adopt a tool when its outputs are checkable and its limits are
stated plainly. Change management here means: publish the rubric,
publish the evidence lists, publish the decision and its reasons,
and let reviewers re-run the same checks later with the same inputs.
