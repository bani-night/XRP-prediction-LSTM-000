from typing import List, Dict, Any, Tuple
import random
import pandas as pd
import numpy as np

from apex.intelligence.strategy_genome import StrategyGenome
from apex.reality.risk_engine import RiskEngine

class StrategyEvolution:
    """
    Evolves trading strategies with a vectorized backtester that includes risk management.
    """

    def __init__(self, config: Dict[str, Any], historical_data: pd.DataFrame):
        self.config = config
        self.historical_data = historical_data
        self.population_size = self.config.get('population', 50)
        self.elite_percentage = self.config.get('elite_percentage', 0.2)
        self.mutation_rate = self.config.get('mutation_rate', 0.1)
        self.population = self._initialize_population()
        self.risk_engine = RiskEngine(config=config.get('reality', {}).get('risk', {}))

    def _initialize_population(self) -> List[StrategyGenome]:
        return [StrategyGenome.create_random_genome() for _ in range(self.population_size)]

    def evolve(self, prediction: str = None):
        for genome in self.population:
            genome.fitness = self._evaluate_fitness_vectorized(genome, prediction)
        # ... (rest of the method is the same)
        self.population.sort(key=lambda g: g.fitness, reverse=True)
        num_elites = int(self.population_size * self.elite_percentage)
        next_generation = self.population[:num_elites]
        while len(next_generation) < self.population_size:
            parent1, parent2 = self._select_parents(self.population)
            offspring = self._crossover(parent1, parent2)
            self._mutate(offspring)
            next_generation.append(offspring)
        self.population = next_generation

    def _evaluate_fitness_vectorized(self, genome: StrategyGenome, prediction: str) -> float:
        df = self.historical_data.copy()

        # --- Generate Entry Signals ---
        buy_signals = pd.Series(False, index=df.index)
        if genome.dna.get('feature_rsi_enabled'):
            buy_signals |= (df['rsi'].shift(1) < genome.dna['rsi_threshold_buy'])
        if genome.dna.get('feature_macd_enabled') and genome.dna.get('macd_crossover_buy_enabled'):
            buy_signals |= (df['macd'].shift(1) > df['macd_signal'].shift(1))
        if genome.dna.get('use_model_prediction') and prediction == 'BULLISH':
            buy_signals |= True

        # --- Initial Position ---
        position = pd.Series(0, index=df.index)
        position[buy_signals] = 1

        # --- Apply Risk Management to Generate Exit Signals ---
        # Note: This is a simplified integration. A full implementation would be more complex.
        # We're using the risk engine to decide when to close the position.
        # For simplicity, we assume the risk engine can modify the position series to close trades.
        # A more realistic simulation would handle this on a trade-by-trade basis.

        # A simple way to integrate exits:
        sell_signals = pd.Series(False, index=df.index)
        if genome.dna.get('feature_rsi_enabled'):
            sell_signals |= (df['rsi'].shift(1) > genome.dna['rsi_threshold_sell'])

        position[sell_signals] = 0
        position = self.risk_engine.manage_risk(df, position, genome.dna)

        # --- Simulate Trades ---
        position.ffill(inplace=True)
        position.fillna(0, inplace=True)

        strategy_returns = df['close'].pct_change() * position.shift(1)

        initial_cash = 10000.0
        portfolio_value = initial_cash * (1 + strategy_returns).cumprod()

        return portfolio_value.iloc[-1] if not portfolio_value.empty else initial_cash

    def _select_parents(self, population: List[StrategyGenome]) -> Tuple[StrategyGenome, StrategyGenome]:
        # ... (same as before)
        pass

    def _crossover(self, parent1: StrategyGenome, parent2: StrategyGenome) -> StrategyGenome:
        # ... (same as before)
        pass

    def _mutate(self, genome: StrategyGenome):
        # ... (same as before)
        pass

if __name__ == '__main__':
    # ... (same as before)
    pass
