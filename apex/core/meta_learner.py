from collections import defaultdict
from typing import Dict, Any, List
import numpy as np

from apex.intelligence.strategy_genome import StrategyGenome

class MetaLearner:
    """
    Learns which strategies are effective under different market regimes.
    It maintains a memory of strategy performance correlated with market state.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # Memory structure: {regime: {phenotype: [fitness_scores]}}
        self.regime_strategy_performance = defaultdict(lambda: defaultdict(list))

    def update_memory(self, market_regime: str, strategies: List[StrategyGenome]):
        """
        Updates the learner's memory with the performance of strategies in a given market regime.
        """
        for strategy in strategies:
            phenotype = self._get_strategy_phenotype(strategy)
            self.regime_strategy_performance[market_regime][phenotype].append(strategy.fitness)

    def select_best_strategy(self, market_regime: str) -> Dict[str, Any]:
        """
        Selects the best-performing strategy phenotype for a given market regime.

        Returns:
            A dictionary representing the best strategy phenotype, or an empty dict if no data.
        """
        if market_regime not in self.regime_strategy_performance:
            return {}

        phenotypes = self.regime_strategy_performance[market_regime]
        if not phenotypes:
            return {}

        # Calculate average fitness for each phenotype
        avg_fitness = {
            phenotype: np.mean(scores) for phenotype, scores in phenotypes.items()
        }

        # Return the phenotype with the highest average fitness
        return max(avg_fitness, key=avg_fitness.get)

    def _get_strategy_phenotype(self, strategy: StrategyGenome) -> str:
        """
        Creates a simplified, hashable representation of a strategy's DNA (its phenotype).
        """
        # Example: "rsi_True_macd_False_model_True"
        return (
            f"rsi_{strategy.dna.get('feature_rsi_enabled', False)}_"
            f"macd_{strategy.dna.get('feature_macd_enabled', False)}_"
            f"model_{strategy.dna.get('use_model_prediction', False)}"
        )
