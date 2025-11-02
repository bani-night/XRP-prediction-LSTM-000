import unittest
import sys
import os

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apex.core.meta_learner import MetaLearner
from apex.intelligence.strategy_genome import StrategyGenome

class TestMetaLearner(unittest.TestCase):

    def test_meta_learner(self):
        """
        Tests the MetaLearner's ability to learn and select the best strategy for a given market regime.
        """
        meta_learner = MetaLearner(config={})

        # --- Simulate a "VOLATILE" market regime ---
        volatile_strategies = [StrategyGenome.create_random_genome() for _ in range(5)]
        volatile_strategies[0].fitness = 12000
        volatile_strategies[0].dna['feature_rsi_enabled'] = True # Explicitly set for the test
        volatile_strategies[1].fitness = 9000
        volatile_strategies[1].dna['feature_rsi_enabled'] = False
        meta_learner.update_memory(market_regime="VOLATILE", strategies=volatile_strategies)

        # --- Simulate a "STABLE" market regime ---
        stable_strategies = [StrategyGenome.create_random_genome() for _ in range(5)]
        stable_strategies[2].fitness = 11000
        stable_strategies[2].dna['feature_macd_enabled'] = True # Explicitly set for the test
        stable_strategies[3].fitness = 9500
        meta_learner.update_memory(market_regime="STABLE", strategies=stable_strategies)

        # --- Test selection ---
        best_volatile_phenotype = meta_learner.select_best_strategy("VOLATILE")
        self.assertIn("rsi_True", best_volatile_phenotype)

        best_stable_phenotype = meta_learner.select_best_strategy("STABLE")
        self.assertIn("macd_True", best_stable_phenotype)

if __name__ == '__main__':
    unittest.main()
