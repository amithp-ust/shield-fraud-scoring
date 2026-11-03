"""Synthetic claim fraud score (CM-FRAUD)."""

import sqlite3


class FraudScoring:
    def __init__(self, policy_database: sqlite3.Connection):
        self.policy_database = policy_database

    def score(self, policy_id: str, requested_cents: int) -> dict:
        if type(requested_cents) is not int or requested_cents <= 0:
            raise ValueError("requested_cents must be a positive integer")
        row = self.policy_database.execute(
            "SELECT coverage_cents, deductible_cents, status "
            "FROM policy_risk_view WHERE policy_id = ?",
            (policy_id,),
        ).fetchone()
        if row is None:
            raise LookupError(f"Policy risk record not found: {policy_id}")
        coverage_cents, deductible_cents, status = row
        score = 10
        if requested_cents > coverage_cents:
            score += 40
        if deductible_cents == 0:
            score += 10
        if status != "active":
            score += 60
        return {"policy_id": policy_id, "score": min(score, 100)}
