import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import List, Dict, Any, Tuple
import random
from apex.intelligence.strategy_genome import StrategyGenome

class StrategyEvolution:
    """
    Evolves trading strategies using a genetic algorithm.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the StrategyEvolution with a configuration.

        Args:
            config: A dictionary containing parameters for the genetic algorithm.
        """
        self.config = config
        self.population_size = self.config.get('population', 50)
        self.genome_length = self.config.get('genome_length', 12)
        self.elite_percentage = self.config.get('elite_percentage', 0.2)
        self.mutation_rate = self.config.get('mutation_rate', 0.1)

        self.population = self._initialize_population()

    def _initialize_population(self) -> List[StrategyGenome]:
        """
        Creates an initial population of random strategies.
        """
        return [StrategyGenome.create_random_genome(self.genome_length) for _ in range(self.population_size)]

    def evolve(self):
        """
        Runs one generation of the genetic algorithm.
        """
        # 1. Evaluate fitness (placeholder)
        for genome in self.population:
            genome.fitness = self._evaluate_fitness(genome)

        # 2. Sort by fitness
        self.population.sort(key=lambda g: g.fitness, reverse=True)

        # 3. Select elites
        num_elites = int(self.population_size * self.elite_percentage)
        next_generation = self.population[:num_elites]

        # 4. Breed new generation
        while len(next_generation) < self.population_size:
            parent1, parent2 = self._select_parents(self.population)
            offspring = self._crossover(parent1, parent2)
            offspring = self._mutate(offspring)
            next_generation.append(offspring)

        self.population = next_generation

    def _evaluate_fitness(self, genome: StrategyGenome) -> float:
        """
        Evaluates the fitness of a single genome.

        Placeholder: Returns a random fitness value.
        In a real system, this would involve backtesting or paper trading.
        """
        return random.uniform(0.1, 5.0)

    def _select_parents(self, population: List[StrategyGenome]) -> Tuple[StrategyGenome, StrategyGenome]:
        """
        Selects two parents from the population for breeding.

        Using tournament selection.
        """
        tournament_size = 5

        def tournament() -> StrategyGenome:
            competitors = random.sample(population, tournament_size)
            competitors.sort(key=lambda g: g.fitness, reverse=True)
            return competitors[0]

        return tournament(), tournament()

    def _crossover(self, parent1: StrategyGenome, parent2: StrategyGenome) -> StrategyGenome:
        """
        Performs crossover between two parents to create an offspring.
        """
        crossover_point = random.randint(1, self.genome_length - 1)
        child_dna = parent1.dna[:crossover_point] + parent2.dna[crossover_point:]
        return StrategyGenome(child_dna)

    def _mutate(self, genome: StrategyGenome) -> StrategyGenome:
        """
        Applies mutation to a genome.
        """
        for i in range(self.genome_length):
            if random.random() < self.mutation_rate:
                genome.dna[i] = random.random() # Simple mutation
        return genome

if __name__ == '__main__':
    mock_config = {
        'population': 50,
        'genome_length': 12,
        'elite_percentage': 0.2,
        'mutation_rate': 0.1
    }

    evolution = StrategyEvolution(config=mock_config)
    print("Initial population created.")
    print(f"  - Population size: {len(evolution.population)}")
    print(f"  - Example genome: {evolution.population[0]}")

    # Run a few generations
    num_generations = 10
    for gen in range(num_generations):
        evolution.evolve()
        best_genome = evolution.population[0]
        print(f"\nGeneration {gen + 1}/{num_generations}")
        print(f"  - Best fitness: {best_genome.fitness:.4f}")

    print("\nEvolution complete.")
    print(f"Final best genome: {evolution.population[0]}")
