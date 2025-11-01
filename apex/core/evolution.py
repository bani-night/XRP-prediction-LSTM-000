from typing import List, Dict, Any, Tuple
import random
import pandas as pd
import numpy as np

from apex.intelligence.strategy_genome import StrategyGenome

class StrategyEvolution:
    """
    Evolves trading strategies using a genetic algorithm with structured genomes.
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

    def evolve(self):
        # 1. Evaluate fitness of each genome in the population
        for genome in self.population:
            genome.fitness = self._evaluate_fitness(genome)

        # 2. Sort the population by fitness in descending order
        self.population.sort(key=lambda g: g.fitness, reverse=True)

        # 3. Select the top performers (elites) for the next generation
        num_elites = int(self.population_size * self.elite_percentage)
        next_generation = self.population[:num_elites]

        # 4. Breed the rest of the new generation from the current generation
        while len(next_generation) < self.population_size:
            parent1, parent2 = self._select_parents(self.population)
            offspring = self._crossover(parent1, parent2)
            self._mutate(offspring)
            next_generation.append(offspring)

        self.population = next_generation

    def _evaluate_fitness(self, genome: StrategyGenome) -> float:
        """
        Evaluates the fitness of a genome by running a simplified backtest on historical data.
        The fitness is defined as the final portfolio value.
        """
        cash = 10000.0
        position = 0.0

        for i in range(1, len(self.historical_data)):
            # Determine buy/sell signals based on the genome's DNA
            buy_signal = self._get_buy_signal(genome, i)
            sell_signal = self._get_sell_signal(genome, i)

            # Execute trades
            current_price = self.historical_data['close'].iloc[i]
            if current_price > 0: # Avoid division by zero
                if buy_signal and cash > 0:
                    position = cash / current_price
                    cash = 0.0
                elif sell_signal and position > 0:
                    cash = position * current_price
                    position = 0.0

        # Calculate the final portfolio value
        final_price = self.historical_data['close'].iloc[-1]
        return cash + position * final_price

    def _get_buy_signal(self, genome: StrategyGenome, index: int) -> bool:
        """Checks for buy signals based on the genome's strategy."""
        if genome.dna['feature_rsi_enabled'] and self.historical_data['rsi'].iloc[index-1] < genome.dna['rsi_threshold_buy']:
            return True
        if genome.dna['feature_macd_enabled'] and genome.dna['macd_crossover_buy_enabled'] and \
           self.historical_data['macd'].iloc[index-1] > self.historical_data['macd_signal'].iloc[index-1]:
            return True
        return False

    def _get_sell_signal(self, genome: StrategyGenome, index: int) -> bool:
        """Checks for sell signals based on the genome's strategy."""
        if genome.dna['feature_rsi_enabled'] and self.historical_data['rsi'].iloc[index-1] > genome.dna['rsi_threshold_sell']:
            return True
        if genome.dna['feature_macd_enabled'] and genome.dna['macd_crossover_sell_enabled'] and \
           self.historical_data['macd'].iloc[index-1] < self.historical_data['macd_signal'].iloc[index-1]:
            return True
        return False

    def _select_parents(self, population: List[StrategyGenome]) -> Tuple[StrategyGenome, StrategyGenome]:
        """Selects two parents using fitness proportionate selection."""
        fitness_scores = [g.fitness for g in population]
        # Handle cases where all fitness scores are zero
        if sum(fitness_scores) == 0:
            return tuple(random.choices(population, k=2))
        return tuple(random.choices(population, k=2, weights=fitness_scores))

    def _crossover(self, parent1: StrategyGenome, parent2: StrategyGenome) -> StrategyGenome:
        """Performs uniform crossover."""
        child_dna = {key: random.choice([parent1.dna[key], parent2.dna[key]]) for key in parent1.dna}
        return StrategyGenome(child_dna)

    def _mutate(self, genome: StrategyGenome):
        """Applies mutation to each gene in the genome."""
        for key in genome.dna:
            if random.random() < self.mutation_rate:
                gene = genome.dna[key]
                if isinstance(gene, bool):
                    genome.dna[key] = not gene
                elif isinstance(gene, int):
                    genome.dna[key] += random.randint(-5, 5)
                elif isinstance(gene, float):
                    genome.dna[key] *= random.uniform(0.8, 1.2)

if __name__ == '__main__':
    from apex.intelligence.pattern_dna import PatternDNA

    mock_config = {
        'population': 50, 'elite_percentage': 0.2, 'mutation_rate': 0.1
    }

    historical_data = pd.DataFrame({'close': np.random.uniform(99, 103, 200) + np.sin(np.linspace(0, 20, 200)) * 5})
    PatternDNA(config={})._add_technical_indicators(historical_data)

    evolution = StrategyEvolution(config=mock_config, historical_data=historical_data)

    for gen in range(10):
        evolution.evolve()
        best_genome = evolution.population[0]
        print(f"Generation {gen + 1}/10 - Best fitness: {best_genome.fitness:.2f}")

    print(f"\nFinal best genome: {evolution.population[0]}")
