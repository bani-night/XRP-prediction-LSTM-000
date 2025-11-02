import time
import yaml
import pandas as pd
import numpy as np
import json
from typing import Dict, Any
import logging

from apex.core.brain import BrainEvolution
from apex.core.evolution import StrategyEvolution
from apex.intelligence.pattern_dna import PatternDNA
from apex.intelligence.prediction_engine import UniversalPredictor
from apex.reality.market_stream import MarketStream
from apex.reality.validator import RealityValidator
from apex.evolution.self_modifier import SelfModifier

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ApexSystem:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.market_stream = MarketStream(config=config.get('reality', {}))
        initial_data = self._get_initial_data()

        self.pattern_dna = PatternDNA(config=config.get('intelligence', {}).get('patterns', {}))
        self.pattern_dna._add_technical_indicators(initial_data)

        self.brain_evolution = BrainEvolution(config=config.get('intelligence', {}).get('brain', {}), historical_data=initial_data)
        self.strategy_evolution = StrategyEvolution(config=config.get('intelligence', {}).get('strategies', {}), historical_data=initial_data)

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
        logging.info("Starting APEX main loop...")
        data_generator = self.market_stream.get_live_data()

        max_cycles = self.config.get('execution', {}).get('max_cycles', 0)
        save_freq = self.config.get('execution', {}).get('save_state_frequency', 0)

        for i, market_data in enumerate(data_generator):
            logging.info(f"--- Cycle {i + 1} ---")

            try:
                # 1. Feature Engineering and Prediction
                intelligence = self.pattern_dna.extract_intelligence(market_data.copy())
                prediction_data = self._prepare_data_for_predictor(intelligence['features'])
                prediction = self.predictor.predict(prediction_data)
                pred_direction = 'BULLISH' if np.mean(prediction) > prediction_data['target'].iloc[-1] else 'BEARISH'
                logging.info(f"Model Prediction: {pred_direction}")

                # 2. Strategy Evolution (now using the prediction)
                self.strategy_evolution.evolve(prediction=pred_direction)
                logging.info(f"Strategies evolved. Best fitness: {self.strategy_evolution.population[0].fitness:.2f}")

                # 3. Validation (of the top strategy)
                top_strategy = self.strategy_evolution.population[0]
                # This validation is simplistic. A more robust validation would run the top strategy
                # on the latest data and see if it's profitable.
                logging.info(f"Top strategy uses model prediction: {top_strategy.dna.get('use_model_prediction')}")


                # 4. State Saving
                if save_freq > 0 and (i + 1) % save_freq == 0:
                    self._save_state()

            except Exception as e:
                logging.error(f"Error in cycle {i+1}: {e}", exc_info=True)

            if max_cycles > 0 and i >= max_cycles - 1:
                logging.info("Max cycles reached. Shutting down.")
                break

    def _save_state(self):
        logging.info("Saving best strategies...")
        best_strategies = [genome.dna for genome in self.strategy_evolution.population[:5]]
        with open("best_strategies.json", "w") as f:
            json.dump(best_strategies, f, indent=4)

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
