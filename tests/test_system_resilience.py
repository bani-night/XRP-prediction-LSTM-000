import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apex.intelligence.pattern_dna import PatternDNA

class TestSystemResilience(unittest.TestCase):

    def test_configurable_feature_engineering(self):
        """
        Tests that the PatternDNA class correctly enables/disables features based on config.
        """
        config = {
            'technical_indicators': {
                'rsi': {'enabled': True, 'window': 14},
                'macd': {'enabled': False},
                'atr': {'enabled': True, 'window': 10}
            }
        }

        pattern_dna = PatternDNA(config=config)

        df = pd.DataFrame({
            'high': np.random.rand(50), 'low': np.random.rand(50),
            'close': np.random.rand(50)
        })

        pattern_dna._add_technical_indicators(df)

        self.assertIn('rsi', df.columns)
        self.assertNotIn('macd', df.columns)
        self.assertIn('atr', df.columns)

    def test_missing_data_handling(self):
        """
        Tests that PatternDNA handles DataFrames with missing columns gracefully.
        """
        pattern_dna = PatternDNA(config={})

        # DataFrame missing the 'high' column
        df = pd.DataFrame({'low': np.random.rand(50), 'close': np.random.rand(50)})

        # This should execute without errors
        try:
            pattern_dna._add_technical_indicators(df)
        except Exception as e:
            self.fail(f"PatternDNA failed to handle missing data gracefully: {e}")

if __name__ == '__main__':
    unittest.main()
