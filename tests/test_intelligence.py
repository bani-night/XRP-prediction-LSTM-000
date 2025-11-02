import unittest
import numpy as np
import pandas as pd

from apex.intelligence.pattern_dna import PatternDNA
from apex.intelligence.prediction_engine import UniversalPredictor
from apex.core.brain import BrainEvolution

class TestIntelligenceCore(unittest.TestCase):

    def test_pattern_dna_initialization(self):
        """Test that PatternDNA can be initialized."""
        mock_config = {'wavelet_levels': [1, 2, 4]}
        pattern_dna = PatternDNA(config=mock_config)
        self.assertIsInstance(pattern_dna, PatternDNA)

    def test_pattern_dna_extraction(self):
        """Test the output structure of PatternDNA's extract_intelligence."""
        mock_config = {'wavelet_levels': [1, 2, 4]}
        pattern_dna = PatternDNA(config=mock_config)
        mock_data = pd.DataFrame({'close': np.random.rand(100), 'high': np.random.rand(100), 'low': np.random.rand(100)})
        intelligence = pattern_dna.extract_intelligence(mock_data)
        self.assertIn('features', intelligence)
        self.assertIn('wavelet_features', intelligence)
        self.assertIn('attention_weights', intelligence)
        self.assertIn('market_regime', intelligence)
        self.assertIn('fractal_dimension', intelligence)

    def test_universal_predictor_initialization(self):
        """Test that UniversalPredictor can be initialized."""
        mock_training_params = {
            "learning_rate": 0.03, "hidden_size": 16, "attention_head_size": 1,
            "dropout": 0.1, "hidden_continuous_size": 8,
        }
        predictor = UniversalPredictor(
            training_parameters=mock_training_params,
            max_prediction_length=20,
            max_encoder_length=60
        )
        self.assertIsInstance(predictor, UniversalPredictor)

    def test_brain_evolution_initialization(self):
        """Test that BrainEvolution can be initialized."""
        mock_config = {'generations': 5}
        mock_data = pd.DataFrame({
            'time_idx': np.arange(100), 'target': np.random.rand(100),
            'group': ['a'] * 100, 'feature1': np.random.rand(100),
            'close': np.random.rand(100), 'high': np.random.rand(100), 'low': np.random.rand(100)
        })
        brain_evolution = BrainEvolution(config=mock_config, historical_data=mock_data)
        self.assertIsInstance(brain_evolution, BrainEvolution)

if __name__ == '__main__':
    unittest.main()
