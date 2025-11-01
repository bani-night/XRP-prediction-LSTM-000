import time
import yaml
from typing import Dict, Any
import numpy as np

from apex.core.brain import BrainEvolution
from apex.core.evolution import StrategyEvolution
from apex.intelligence.pattern_dna import PatternDNA
from apex.intelligence.prediction_engine import UniversalPredictor
from apex.reality.market_stream import MarketStream
from apex.reality.validator import RealityValidator
from apex.evolution.self_modifier import SelfModifier

class ApexSystem:
    """
    The main orchestrator for the APEX prediction system.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the entire APEX system with a given configuration.
        """
        self.config = config

        # Initialize all components
        self.brain_evolution = BrainEvolution(config=config.get('intelligence', {}).get('brain', {}))
        self.strategy_evolution = StrategyEvolution(config=config.get('intelligence', {}).get('strategies', {}))
        self.pattern_dna = PatternDNA(config=config.get('intelligence', {}).get('patterns', {}))

        # We need to get the best architecture from the brain evolution to initialize the predictor
        # For this placeholder, we'll use some mock training params
        mock_training_params = {
            "learning_rate": 0.03, "hidden_size": 16, "attention_head_size": 1,
            "dropout": 0.1, "hidden_continuous_size": 8,
        }
        self.predictor = UniversalPredictor(config={}, training_parameters=mock_training_params)

        self.market_stream = MarketStream(config=config.get('reality', {}))
        self.validator = RealityValidator(config=config.get('reality', {}))
        self.self_modifier = SelfModifier(config=config.get('evolution', {}))

    def run_evolution_loop(self):
        """
        Runs the main evolution loop of the APEX system.
        """
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                    APEX PREDICTION SYSTEM                      ║")
        print("║                     Market Intelligence                        ║")
        print("╚════════════════════════════════════════════════════════════════╝")

        data_generator = self.market_stream.get_live_data()

        for i, market_data in enumerate(data_generator):
            print(f"\n--- Cycle {i + 1} ---")

            # 1. Analyze market data
            numeric_market_data = market_data.select_dtypes(include=np.number)
            intelligence = self.pattern_dna.extract_intelligence(numeric_market_data.values)
            print(f"[INTELLIGENCE CORE] Market Regime: {intelligence['market_regime']}")

            # 2. Make prediction
            prediction = self.predictor.predict(market_data)
            print(f"[PREDICTION] Prediction generated.")

            # 3. Validate prediction
            validation_result = self.validator.validate_prediction(prediction, market_data)
            print(f"[REALITY ENGINE] Prediction validated. Correct: {validation_result['is_correct']}")

            # 4. Evolve strategies
            self.strategy_evolution.evolve()
            best_strategy = self.strategy_evolution.population[0]
            print(f"[EVOLUTION] Strategies evolved. Best fitness: {best_strategy.fitness:.4f}")

            # 5. Evolve architecture (less frequently)
            if i % 5 == 0: # Evolve architecture every 5 cycles
                print("[BRAIN] Evolving architecture...")
                # In a real system, this would be a long process.
                # best_params = self.brain_evolution.evolve_architecture()
                # self.predictor = UniversalPredictor(config={}, training_parameters=best_params)
                print("[BRAIN] Architecture evolution complete.")

            # 6. Self-modify (if enabled)
            self.self_modifier.optimize_self()

            time.sleep(1)

            if i >= 9: # Stop after 10 cycles for this example
                break

if __name__ == '__main__':
    # Load configuration from genesis.yaml
    try:
        with open('apex/config/genesis.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: genesis.yaml not found. Please ensure the configuration file exists.")
        exit(1)

    apex_system = ApexSystem(config=config)
    apex_system.run_evolution_loop()
