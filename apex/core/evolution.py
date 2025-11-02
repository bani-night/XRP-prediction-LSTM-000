from typing import List, Dict, Any, Tuple
import random
import pandas as pd
import numpy as np

from apex.intelligence.strategy_genome import StrategyGenome

class StrategyEvolution:
    """
    Evolves trading strategies by evaluating their performance against historical data,
    incorporating both technical indicators and model predictions.
    """

    def __init__(self, config: Dict[str, Any], historical_data: pd.DataFrame):
        self.config = config
        self.historical_data = historical_data
        self.population_size = self.config.get('population', 50)
        self.elite_percentage = self.config.get('elite_percentage', 0.2)
        self.mutation_rate = self.config.get('mutation_rate', 0.1)
        self.population = self._initialize_population()

    def _initialize_population(self) -> List[StrategyGenome]:
        return [StrategyGenome.create_random_genome() for _ in range(self.population_size)]

    def evolve(self, prediction: str = None):
        """
        Runs one generation of the genetic algorithm.

        Args:
            prediction: The prediction from the UniversalPredictor ('BULLISH' or 'BEARISH').
        """
        for genome in self.population:
            genome.fitness = self._evaluate_fitness_vectorized(genome, prediction)

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
        """
        Evaluates fitness using a vectorized backtest that incorporates the model's prediction.
        """
        df = self.historical_data.copy()

        # --- Generate Signals from Technical Indicators ---
        buy_signals = pd.Series(False, index=df.index)
        sell_signals = pd.Series(False, index=df.index)

        if genome.dna.get('feature_rsi_enabled'):
            buy_signals |= (df['rsi'].shift(1) < genome.dna['rsi_threshold_buy'])
            sell_signals |= (df['rsi'].shift(1) > genome.dna['rsi_threshold_sell'])

        if genome.dna.get('feature_macd_enabled'):
            if genome.dna.get('macd_crossover_buy_enabled'):
                buy_signals |= (df['macd'].shift(1) > df['macd_signal'].shift(1))
            if genome.dna.get('macd_crossover_sell_enabled'):
                sell_signals |= (df['macd'].shift(1) < df['macd_signal'].shift(1))

        # --- Incorporate Model Prediction ---
        if genome.dna.get('use_model_prediction') and prediction:
            if prediction == 'BULLISH':
                buy_signals |= True # Strong buy signal across the period
            elif prediction == 'BEARISH':
                sell_signals |= True # Strong sell signal

        # --- Simulate Trades ---
        position = pd.Series(np.nan, index=df.index)
        position[buy_signals] = 1
        position[sell_signals] = 0
        position.ffill(inplace=True)
        position.fillna(0, inplace=True)

        strategy_returns = df['close'].pct_change() * position.shift(1)

        initial_cash = 10000.0
        portfolio_value = initial_cash * (1 + strategy_returns).cumprod()

        return portfolio_value.iloc[-1] if not portfolio_value.empty else initial_cash


    def _select_parents(self, population: List[StrategyGenome]) -> Tuple[StrategyGenome, StrategyGenome]:
        # ... (same as before)
        fitness_scores = [g.fitness for g in population]
        if sum(fitness_scores) == 0: return tuple(random.choices(population, k=2))
        return tuple(random.choices(population, k=2, weights=fitness_scores))

    def _crossover(self, parent1: StrategyGenome, parent2: StrategyGenome) -> StrategyGenome:
        # ... (same as before)
        child_dna = {key: random.choice([parent1.dna[key], parent2.dna[key]]) for key in parent1.dna}
        return StrategyGenome(child_dna)

    def _mutate(self, genome: StrategyGenome):
        # ... (same as before)
        for key in genome.dna:
            if random.random() < self.mutation_rate:
                gene = genome.dna[key]
                if isinstance(gene, bool): genome.dna[key] = not gene
                elif isinstance(gene, int): genome.dna[key] += random.randint(-5, 5)
                elif isinstance(gene, float): genome.dna[key] *= random.uniform(0.8, 1.2)

if __name__ == '__main__':
    # ... (same as before)
    pass
