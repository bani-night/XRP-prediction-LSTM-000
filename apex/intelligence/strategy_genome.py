from typing import List, Any, Dict
import random

class StrategyGenome:
    """
    Represents the DNA of a trading strategy with a structured genome.
    The genome defines the features, parameters, and thresholds for the strategy.
    """

    def __init__(self, dna: Dict[str, Any]):
        """
        Initializes the StrategyGenome.

        Args:
            dna: A dictionary representing the strategy's structured DNA.
        """
        self.dna = dna
        self.fitness = 0.0

    def __repr__(self):
        return f"StrategyGenome(dna={self.dna}, fitness={self.fitness:.4f})"

    @staticmethod
    def create_random_genome() -> 'StrategyGenome':
        """
        Creates a new random genome with a structured and meaningful representation.
        """
        dna = {
            'feature_rsi_enabled': random.choice([True, False]),
            'feature_macd_enabled': random.choice([True, False]),
            'feature_bbands_enabled': random.choice([True, False]),
            'rsi_threshold_buy': random.randint(20, 40),
            'rsi_threshold_sell': random.randint(60, 80),
            'macd_crossover_buy_enabled': random.choice([True, False]),
            'macd_crossover_sell_enabled': random.choice([True, False]),
            'stop_loss_pct': random.uniform(0.01, 0.1),
            'take_profit_pct': random.uniform(0.02, 0.15),
        }
        return StrategyGenome(dna)

if __name__ == '__main__':
    random_genome = StrategyGenome.create_random_genome()
    random_genome.fitness = random.uniform(0.5, 2.5)

    print("Created a random, structured Strategy Genome:")
    print(random_genome)

    # Example of accessing a gene
    print(f"\nExample gene - RSI Buy Threshold: {random_genome.dna['rsi_threshold_buy']}")
