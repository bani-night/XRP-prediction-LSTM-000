import unittest
import pandas as pd
import numpy as np
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apex.core.evolution import StrategyEvolution
from apex.intelligence.pattern_dna import PatternDNA
from apex.intelligence.strategy_genome import StrategyGenome

# A simple, iterative backtester to serve as a reference for correctness
def iterative_backtester(df: pd.DataFrame, genome: StrategyGenome, prediction: str = None) -> float:
    cash = 10000.0
    position = 0.0
    for i in range(1, len(df)):
        buy_signal = False
        sell_signal = False

        if genome.dna['feature_rsi_enabled']:
            if df['rsi'].iloc[i-1] < genome.dna['rsi_threshold_buy']:
                buy_signal = True
            if df['rsi'].iloc[i-1] > genome.dna['rsi_threshold_sell']:
                sell_signal = True

        if genome.dna.get('use_model_prediction') and prediction:
            if prediction == 'BULLISH':
                buy_signal = True
            elif prediction == 'BEARISH':
                sell_signal = True

        if buy_signal and cash > 0:
            position = cash / df['close'].iloc[i]
            cash = 0.0
        elif sell_signal and position > 0:
            cash = position * df['close'].iloc[i]
            position = 0.0
    return cash + position * df['close'].iloc[-1]

class TestEvolutionPerformance(unittest.TestCase):

    def setUp(self):
        """Set up a standard environment for each test."""
        self.mock_config = {'population': 50}
        self.historical_data = pd.DataFrame({
            'high': np.array([105, 106, 104, 107, 108]),
            'low': np.array([100, 101, 102, 103, 104]),
            'close': np.array([101, 102, 103, 105, 106])
        })
        PatternDNA(config={'technical_indicators': {'rsi': {'enabled': True}, 'macd': {'enabled': False}}})._add_technical_indicators(self.historical_data)
        self.evolution = StrategyEvolution(config=self.mock_config, historical_data=self.historical_data)

    def test_vectorized_backtester_correctness(self):
        """
        Ensures the vectorized backtester produces the same result as a simple iterative one.
        """
        genome = StrategyGenome.create_random_genome()
        genome.dna['feature_rsi_enabled'] = True
        genome.dna['rsi_threshold_buy'] = 30
        genome.dna['rsi_threshold_sell'] = 70
        genome.dna['feature_macd_enabled'] = False
        genome.dna['use_model_prediction'] = False

        # Test with no prediction
        vectorized_fitness = self.evolution._evaluate_fitness_vectorized(genome, prediction=None)
        iterative_fitness = iterative_backtester(self.historical_data, genome, prediction=None)
        self.assertAlmostEqual(vectorized_fitness, iterative_fitness, places=5)

        # Test with a BULLISH prediction
        genome.dna['use_model_prediction'] = True
        vectorized_fitness = self.evolution._evaluate_fitness_vectorized(genome, prediction='BULLISH')
        iterative_fitness = iterative_backtester(self.historical_data, genome, prediction='BULLISH')
        self.assertAlmostEqual(vectorized_fitness, iterative_fitness, places=5)


    def test_vectorized_backtester_performance(self):
        pass

if __name__ == '__main__':
    unittest.main()
