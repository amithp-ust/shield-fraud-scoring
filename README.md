# Shield fraud scoring

**Application:** Claims (`claims`)

**Component:** `CM-FRAUD`

**Owner:** Claims platform

`src/fraud/scoring.py` computes a synthetic score from 0 to 100 for claim review.
Supply a SQLite connection with the required data schema; it does not create or
seed a database. `contracts/fraud-api.yaml` describes the intended API.

Shared context: `amithp-ust/shield-context` (`AGENTS.md`, glossary, scope,
standards, and component map). `specs/` is reserved for spec pull requests.
Python 3.12+, standard library only. Run `python -m unittest discover -s tests`.
This callable fixture is not a production fraud model or an HTTP server.
