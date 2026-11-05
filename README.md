# Shield fraud scoring

**Application:** Claims (`claims`)

**Component:** `CM-FRAUD`

**Owner:** Claims platform

`src/fraud/scoring.py` computes a synthetic score from 0 to 100 for claim review.
Supply a SQLite connection with the required data schema; it does not create or
seed a database. `contracts/fraud-api.yaml` describes the intended API.

`CM-FRAUD` depends on `CM-POLICY`: `policy_database` must expose the
`policy_risk_view` created by the policy service's `db/migrations/001_policy.sql`.
`contracts/policy-risk-view.json` links the canonical row schema in
[`shield-policy-service/contracts/shared/policy-risk-view.json`](https://github.com/amithp-ust/shield-policy-service/blob/main/contracts/shared/policy-risk-view.json).
Fraud SELECTs `coverage_cents`, `deductible_cents`, and `status` by `policy_id`;
it does not write the view. Missing rows raise `LookupError`; a missing view
raises `sqlite3.OperationalError`. This documents existing local fixture access,
not client approval of production database sharing.
Run `python scripts/verify_fixture.py --repos-root ..` from the sibling context
checkout to check the provider migration, canonical schema, and consumer link
without fetching remote schemas. Coordinate contract changes with Policy platform.
## Specification consumer

Canonical specs, authoring, gates, and requirement metrics live only in
[`amithp-ust/Intent-to-spec`](https://github.com/amithp-ust/Intent-to-spec).
Shared glossary, map, standards, and policy remain in
[`amithp-ust/shield-context`](https://github.com/amithp-ust/shield-context).
This repo owns `CM-FRAUD` implementation, not spec authoring. See
[AGENTS.md](AGENTS.md) for immutable approved spec references, issue/PR traceability,
human review, and fixture-contract checks. Do not install authoring here or copy
specs; empty `specs/.gitkeep` is a legacy placeholder.

Python 3.11+, standard library only. Run `python -m unittest discover -s tests`
from this repository root; the unit-test CI runs the same command on Python 3.11.
This callable fixture is not a production fraud model or an HTTP server.
