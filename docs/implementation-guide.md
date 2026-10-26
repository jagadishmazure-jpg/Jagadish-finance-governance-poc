# Implementation guide (for adopters)

1. Copy the pattern, not the scores. Replace the synthetic pillar
   scores with your own review rubric, and keep the fail-closed rule:
   a weak pillar must block, whatever the average says.
2. Set the threshold deliberately. The default is 60. Record who set
   it and why; a threshold nobody owns will drift.
3. Price with dated inputs. Store the price date next to every model
   option in your own system. This scaffold's prices are invented.
4. Define evidence items before you grade. Publish the list each
   grade needs, then grade only against it. Never grade from a slide.
5. Keep the authorizer pattern: expose views, never base tables, to
   any reporting query. Deny writes and schema changes in the same
   authorizer, and test denials by exception type.
6. Keep gates boring. One approval path, one named approver, one
   scope, one expiry, one use. If a workflow needs a second path,
   that is a new gate with its own tests, not an exception.
7. Redact before logging. Run outputs through the redactor before
   they reach logs, tickets, or emails, and keep card and email
   patterns in the checklist alongside phone and SSN.
8. Cap every fetch. Use `fetchmany(MAX+1)` and treat over-cap as an
   error the caller must handle, not a page to trim quietly.
