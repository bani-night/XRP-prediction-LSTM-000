import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apex.reality.risk_engine import RiskEngine

class TestRiskEngine(unittest.TestCase):

    def test_risk_engine(self):
        risk_engine = RiskEngine(config={})
        genome = {'stop_loss_pct': 0.1, 'take_profit_pct': 0.2}

        df = pd.DataFrame({
            'high':  [105, 121, 108, 95, 112],
            'low':   [98,  102, 89,  91, 108],
            'close': [100, 110, 105, 92, 110]
        })

        # --- Test Case ---
        position = pd.Series([1, 1, 1, 1, 1]) # Assume we are in a position

        # Expected position after risk management:
        # Index 0: Position is 1 (entry)
        # Index 1: Position becomes 0 (take-profit triggered by high of 121)
        # Index 2: Position remains 0
        # Index 3: Position remains 0
        # Index 4: Position remains 0
        expected_position = [1, 0, 0, 0, 0]

        managed_position = risk_engine.manage_risk(df, position, genome)

        self.assertEqual(managed_position.tolist(), expected_position)

if __name__ == '__main__':
    unittest.main()
