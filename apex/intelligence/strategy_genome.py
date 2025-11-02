from typing import List, Any, Dict
import random

class StrategyGenome:
    """
    Represents the DNA of a trading strategy with a structured genome.
    """

    def __init__(self, dna: Dict[str, Any]):
        self.dna = dna
        self.fitness = 0.0

    def __repr__(self):
        return f"StrategyGenome(dna={self.dna}, fitness={self.fitness:.4f})"

    @staticmethod
    def create_random_genome() -> 'StrategyGenome':
        """
        Creates a new random genome with genes for using technical indicators and model predictions.
        """
        dna = {
            # --- Technical Indicator Genes ---
            'feature_rsi_enabled': random.choice([True, False]),
            'rsi_threshold_buy': random.randint(20, 40),
            'rsi_threshold_sell': random.randint(60, 80),

            'feature_macd_enabled': random.choice([True, False]),
            'macd_crossover_buy_enabled': random.choice([True, False]),
            'macd_crossover_sell_enabled': random.choice([True, False]),

            # --- Model Prediction Gene ---
            'use_model_prediction': random.choice([True, False]),

            # --- Risk Management Genes ---
            'stop_loss_pct': random.uniform(0.01, 0.1),
            'take_profit_pct': random.uniform(0.02, 0.15),
        }
        return StrategyGenome(dna)

if __name__ == '__main__':
    random_genome = StrategyGenome.create_random_genome()
    print(random_genome)
