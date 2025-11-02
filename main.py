import time
import yaml
import pandas as pd
import numpy as np
import json
from typing import Dict, Any
import logging

from apex.core.brain import BrainEvolution
from apex.core.evolution import StrategyEvolution
from apex.core.meta_learner import MetaLearner
from apex.intelligence.pattern_dna import PatternDNA
from apex.intelligence.prediction_engine import UniversalPredictor
from apex.reality.market_stream import MarketStream
from apex.reality.validator import RealityValidator
from apex.evolution.self_modifier import SelfModifier
from apex.evolution.performance_dna import PerformanceDNA
from apex.evolution.knowledge_graph import KnowledgeGraph

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ApexSystem:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.market_stream = MarketStream(config=config.get('reality', {}))
        initial_data = self._get_initial_data()

        # Initialize all components, including the new ones
        self.pattern_dna = PatternDNA(config=config.get('intelligence', {}).get('patterns', {}))
        self.pattern_dna._add_technical_indicators(initial_data)

        self.brain_evolution = BrainEvolution(config=config.get('intelligence', {}).get('brain', {}), historical_data=initial_data)
        self.strategy_evolution = StrategyEvolution(config=config.get('intelligence', {}).get('strategies', {}), historical_data=initial_data)

        self.meta_learner = MetaLearner(config={})
        self.performance_dna = PerformanceDNA(config={})
        self.knowledge_graph = KnowledgeGraph(config={})

        self._initialize_predictor(initial_data)

        self.validator = RealityValidator(config=config.get('reality', {}))
        self.self_modifier = SelfModifier(config=config.get('evolution', {}))

    def _get_initial_data(self) -> pd.DataFrame:
        return next(self.market_stream.get_live_data())

    def _initialize_predictor(self, historical_data: pd.DataFrame):
        logging.info("Initializing predictor...")
        best_params = self.brain_evolution.evolve_architecture()
        logging.info(f"Best initial params: {best_params}")
        self.predictor = UniversalPredictor(training_parameters=best_params, max_prediction_length=20, max_encoder_length=60)
        train_df = self._prepare_data_for_predictor(historical_data)
        self.predictor.train(train_df)
        logging.info("Initial model training complete.")


    def run_evolution_loop(self):
        logging.info("Starting APEX main loop with full learning capabilities...")
        data_generator = self.market_stream.get_live_data()

        max_cycles = self.config.get('execution', {}).get('max_cycles', 10)

        for i, market_data in enumerate(data_generator):
            logging.info(f"--- Cycle {i + 1} ---")

            try:
                # 1. Intelligence Gathering
                intelligence = self.pattern_dna.extract_intelligence(market_data.copy())
                market_regime = intelligence['market_regime']

                # 2. Prediction
                prediction_data = self._prepare_data_for_predictor(intelligence['features'])
                prediction_output = self.predictor.predict(prediction_data)
                pred_direction = 'BULLISH' if np.mean(prediction_output) > prediction_data['target'].iloc[-1] else 'BEARISH'
                logging.info(f"Prediction: {pred_direction} in {market_regime} market.")

                # 3. Strategy Evolution
                self.strategy_evolution.evolve(prediction=pred_direction)
                top_strategy = self.strategy_evolution.population[0]

                # 4. Validation
                validation_result = self.validator.validate_prediction({'direction': pred_direction}, market_data)

                # 5. Update Learning Components
                self.performance_dna.update(pred_direction, validation_result)
                self.meta_learner.update_memory(market_regime, self.strategy_evolution.population)
                self.knowledge_graph.update_graph(
                    market_regime,
                    self.meta_learner._get_strategy_phenotype(top_strategy),
                    pred_direction,
                    validation_result['is_correct']
                )

                # 6. Log Performance
                perf_metrics = self.performance_dna.get_performance_metrics()
                logging.info(f"  Win Rate: {perf_metrics['win_rate']:.2%}")
                logging.info(f"  Best Strategy Fitness: {top_strategy.fitness:.2f}")

            except Exception as e:
                logging.error(f"Error in cycle {i+1}: {e}", exc_info=True)

            if max_cycles > 0 and i >= max_cycles - 1:
                break

        logging.info("--- Run Finished ---")
        logging.info(f"Final Performance: {self.performance_dna.get_performance_metrics()}")

    def _prepare_data_for_predictor(self, df: pd.DataFrame) -> pd.DataFrame:
        df['time_idx'] = np.arange(len(df))
        df['group'] = 'live_data'
        df['target'] = df['close']
        return df

def main():
    try:
        with open('apex/config/genesis.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        logging.error("genesis.yaml not found.")
        exit(1)

    apex_system = ApexSystem(config=config)
    apex_system.run_evolution_loop()

if __name__ == '__main__':
    main()
