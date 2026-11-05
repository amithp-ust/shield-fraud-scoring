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
Keep a full intent package in its primary owning app repo and only linked
component-specific requirement slices in other repos; none are generated here.

Shared context: `amithp-ust/shield-context` (`AGENTS.md`, glossary, scope,
standards, and component map). `specs/` is reserved for spec pull requests.
Python 3.12+, standard library only. Run `python -m unittest discover -s tests`.
This callable fixture is not a production fraud model or an HTTP server.
