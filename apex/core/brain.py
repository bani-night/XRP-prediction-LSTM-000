import optuna
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
import sys
import os
from sklearn.model_selection import train_test_split
import lightning.pytorch as pl
from torch.utils.data import DataLoader

from apex.intelligence.prediction_engine import UniversalPredictor

class BrainEvolution:
    """
    Discovers optimal neural architecture through evolution using Optuna,
    with a proper validation set to prevent overfitting.
    """

    def __init__(self, config: Dict[str, Any], historical_data: pd.DataFrame):
        self.config = config
        # Split data into training and validation sets
        self.train_data, self.validation_data = train_test_split(historical_data, test_size=0.2, shuffle=False)
        self.study = optuna.create_study(direction="minimize") # Minimize validation loss

    def evolve_architecture(self) -> Dict[str, Any]:
        self.study.optimize(self._objective, n_trials=self.config.get('generations', 10))
        return self.study.best_params

    def _objective(self, trial: optuna.Trial) -> float:
        """
        Trains a model with a given set of hyperparameters and evaluates it on the validation set.
        """
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-1, log=True),
            "hidden_size": trial.suggest_int("hidden_size", 16, 64),
            "attention_head_size": trial.suggest_int("attention_head_size", 1, 4),
            "dropout": trial.suggest_float("dropout", 0.1, 0.4),
            "hidden_continuous_size": trial.suggest_int("hidden_continuous_size", 8, 32),
        }

        try:
            predictor = UniversalPredictor(
                training_parameters=params,
                max_prediction_length=20,
                max_encoder_length=60
            )

            # Train the model on the training set
            predictor.train(self.train_data)

            # Evaluate the model on the validation set
            validation_dataset = predictor.create_dataset(self.validation_data)
            val_dataloader = validation_dataset.to_dataloader(train=False, batch_size=64)

            # Use the PyTorch Lightning trainer to get validation loss
            trainer = pl.Trainer(accelerator="cpu", logger=False)
            validation_results = trainer.validate(predictor.model, val_dataloader)

            return validation_results[0]['val_loss']

        except Exception as e:
            print(f"Trial failed with error: {e}")
            return float('inf')

if __name__ == '__main__':
    mock_config = {'generations': 5}

    data_size = 300 # Increased size for a more meaningful train/validation split
    mock_historical_data = pd.DataFrame({
        'time_idx': np.arange(data_size),
        'target': np.random.randn(data_size),
        'group': ['stock_A'] * data_size,
        'feature1': np.random.randn(data_size)
    })

    brain_evolution = BrainEvolution(config=mock_config, historical_data=mock_historical_data)

    print("Starting architecture evolution with proper validation...")
    best_params = brain_evolution.evolve_architecture()

    print("\nEvolution complete.")
    print("Best hyperparameters found:")
    for key, value in best_params.items():
        print(f"  {key}: {value}")
