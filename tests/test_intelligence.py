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
        mock_data = np.random.rand(100, 10)
        intelligence = pattern_dna.extract_intelligence(mock_data)
        self.assertIn('wavelet_features', intelligence)
        self.assertIn('attention_weights', intelligence)
        self.assertIn('market_regime', intelligence)
        self.assertIn('fractal_dimension', intelligence)

    def test_universal_predictor_initialization(self):
        """Test that UniversalPredictor can be initialized."""
        mock_config = {'prediction_length': 20}
        mock_training_params = {
            "learning_rate": 0.03,
            "hidden_size": 16,
            "attention_head_size": 1,
            "dropout": 0.1,
            "hidden_continuous_size": 8,
        }
        predictor = UniversalPredictor(config=mock_config, training_parameters=mock_training_params)
        self.assertIsInstance(predictor, UniversalPredictor)

    def test_brain_evolution_initialization(self):
        """Test that BrainEvolution can be initialized."""
        mock_config = {'generations': 5}
        brain_evolution = BrainEvolution(config=mock_config)
        self.assertIsInstance(brain_evolution, BrainEvolution)

if __name__ == '__main__':
    unittest.main()
