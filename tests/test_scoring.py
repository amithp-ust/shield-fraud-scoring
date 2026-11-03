import sqlite3
import unittest

from src.fraud.scoring import FraudScoring


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.connection.executescript("""
            CREATE TABLE policies (
                policy_id TEXT, coverage_cents INTEGER,
                deductible_cents INTEGER, status TEXT
            );
            CREATE VIEW policy_risk_view AS SELECT * FROM policies;
            INSERT INTO policies VALUES ('P-1', 100000, 10000, 'active');
            INSERT INTO policies VALUES ('P-2', 100000, 0, 'cancelled');
        """)
        self.scoring = FraudScoring(self.connection)

    def test_score(self):
        self.assertEqual(self.scoring.score("P-1", 50000)["score"], 10)
        self.assertEqual(self.scoring.score("P-1", 100001)["score"], 50)
        self.assertEqual(self.scoring.score("P-2", 100001)["score"], 100)

    def test_missing_policy(self):
        with self.assertRaises(LookupError):
            self.scoring.score("unknown", 1000)

    def test_invalid_amount(self):
        for amount in (0, -1, 1.5, True):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.scoring.score("P-1", amount)
