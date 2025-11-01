import time
import yaml
import pandas as pd
import numpy as np
from typing import Dict, Any
import logging
import sys
import os

from apex.core.brain import BrainEvolution
from apex.core.evolution import StrategyEvolution
from apex.intelligence.pattern_dna import PatternDNA
from apex.intelligence.prediction_engine import UniversalPredictor
from apex.reality.market_stream import MarketStream
from apex.reality.validator import RealityValidator
from apex.evolution.self_modifier import SelfModifier

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ApexSystem:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

        # Initialize components
        self.market_stream = MarketStream(config=config.get('reality', {}))
        initial_data = next(self.market_stream.get_live_data())

        self.pattern_dna = PatternDNA(config=config.get('intelligence', {}).get('patterns', {}))
        self.pattern_dna._add_technical_indicators(initial_data)

        self.brain_evolution = BrainEvolution(config=config.get('intelligence', {}).get('brain', {}), historical_data=initial_data)
        self.strategy_evolution = StrategyEvolution(config=config.get('intelligence', {}).get('strategies', {}), historical_data=initial_data)

        # Evolve and initialize the prediction model
        self._initialize_predictor(initial_data)

        self.validator = RealityValidator(config=config.get('reality', {}))
        self.self_modifier = SelfModifier(config=config.get('evolution', {}))

    def _initialize_predictor(self, historical_data: pd.DataFrame):
        """Evolves the architecture and trains the initial model."""
        logging.info("Performing initial brain evolution to find optimal architecture...")
        best_params = self.brain_evolution.evolve_architecture()
        logging.info(f"Best initial params found: {best_params}")

        self.predictor = UniversalPredictor(
            training_parameters=best_params,
            max_prediction_length=20, max_encoder_length=60
        )

        logging.info("Training the initial prediction model...")
        train_df = self._prepare_data_for_predictor(historical_data)
        self.predictor.train(train_df)
        logging.info("Initial model training complete.")

    def run_evolution_loop(self):
        logging.info("Starting APEX Prediction System main loop...")
        data_generator = self.market_stream.get_live_data()

        for i, market_data in enumerate(data_generator):
            logging.info(f"--- Cycle {i + 1} ---")

            try:
                # 1. Feature Engineering
                intelligence = self.pattern_dna.extract_intelligence(market_data.copy())
                logging.info(f"Market Regime: {intelligence['market_regime']}")

                # 2. Prediction
                prediction_data = self._prepare_data_for_predictor(intelligence['features'])
                prediction = self.predictor.predict(prediction_data)

                # Simple prediction logic
                last_known_price = prediction_data['target'].iloc[-1]
                pred_direction = 'BULLISH' if np.mean(prediction) > last_known_price else 'BEARISH'
                logging.info(f"Prediction: {pred_direction}")

                # 3. Validation
                validation_result = self.validator.validate_prediction({'direction': pred_direction}, market_data)
                logging.info(f"Validation: Correct={validation_result['is_correct']}, P/L %={validation_result.get('profit_loss_pct', 0):.4f}")

                # 4. Strategy Evolution
                self.strategy_evolution.evolve()
                logging.info(f"Strategies evolved. Best fitness: {self.strategy_evolution.population[0].fitness:.2f}")

            except Exception as e:
                logging.error(f"An error occurred in cycle {i+1}: {e}", exc_info=True)

            if self.config.get('max_cycles') and i >= self.config['max_cycles'] - 1:
                logging.info("Maximum cycles reached. Shutting down.")
                break

    def _prepare_data_for_predictor(self, df: pd.DataFrame) -> pd.DataFrame:
        predictor_df = df.copy()
        predictor_df['time_idx'] = np.arange(len(predictor_df))
        predictor_df['group'] = 'live_data'
        predictor_df['target'] = predictor_df['close']
        return predictor_df

def main():
    try:
        with open('apex/config/genesis.yaml', 'r') as f:
            config = yaml.safe_load(f)
            config['max_cycles'] = 5 # Add a max cycles limit for the example run
    except FileNotFoundError:
        logging.error("genesis.yaml not found.")
        exit(1)

    apex_system = ApexSystem(config=config)
    apex_system.run_evolution_loop()

if __name__ == '__main__':
    main()
