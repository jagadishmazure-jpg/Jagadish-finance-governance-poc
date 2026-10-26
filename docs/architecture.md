# Architecture

```mermaid
flowchart TD
    A[Reviewer input: synthetic initiative] --> B[Scorecard]
    A --> C[PoC economics]
    A --> D[CIA checklist]
    A --> E[Build vs buy]
    A --> F[Evidence grader]
    B --> G[Fail-closed recommendation]
    C --> G
    D --> G
    E --> G
    F --> G
    G --> H[Confirmation gate + named approval]
    H --> I[Go / blocked decision]
    J[View-aware SQLite store] --> B
    J --> F
    K[PII redactor] --> J
    K --> H
```

Modules map one-to-one to the five jobs: `scorecard`, `economics`,
`cia`, `build_buy`, `evidence`. Cross-cutting controls live in
`approvals`, `gates`, `pii`, `store`, `notify`, and `brand`.
Nothing calls the network. Storage is an in-memory database behind a
view-only authorizer.
