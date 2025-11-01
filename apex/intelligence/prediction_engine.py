import torch
from torch.utils.data import DataLoader
from pytorch_forecasting import TemporalFusionTransformer, TimeSeriesDataSet
from pytorch_forecasting.data import GroupNormalizer
from pytorch_forecasting.metrics import QuantileLoss
import pandas as pd
import numpy as np
from typing import Dict, Any, List
import lightning.pytorch as pl

class UniversalPredictor:
    """
    Single adaptive architecture based on the Temporal Fusion Transformer.
    """

    def __init__(self, training_parameters: Dict[str, Any], max_prediction_length: int, max_encoder_length: int):
        self.training_parameters = training_parameters
        self.max_prediction_length = max_prediction_length
        self.max_encoder_length = max_encoder_length
        self.model = None

    def create_dataset(self, data: pd.DataFrame) -> TimeSeriesDataSet:
        """
        Creates a TimeSeriesDataSet for the Temporal Fusion Transformer.
        """
        return TimeSeriesDataSet(
            data,
            time_idx="time_idx",
            target="target",
            group_ids=["group"],
            max_encoder_length=self.max_encoder_length,
            max_prediction_length=self.max_prediction_length,
            static_categoricals=["group"],
            time_varying_known_reals=["time_idx"],
            time_varying_unknown_reals= [col for col in data.columns if col not in ['time_idx', 'target', 'group']],
            target_normalizer=GroupNormalizer(groups=["group"], transformation="softplus"),
        )

    def train(self, train_data: pd.DataFrame):
        """
        Trains the Temporal Fusion Transformer model.
        """
        training_dataset = self.create_dataset(train_data)

        # Create a dataloader for training
        train_dataloader = training_dataset.to_dataloader(train=True, batch_size=64, num_workers=4)

        # Initialize the trainer
        trainer = pl.Trainer(
            max_epochs=2, # Keep it short for this example
            accelerator="cpu",
            gradient_clip_val=0.1,
            limit_train_batches=50,
            enable_checkpointing=False,
            logger=False,
            callbacks=[],
        )

        # Initialize the model
        self.model = TemporalFusionTransformer.from_dataset(
            training_dataset,
            **self.training_parameters,
        )

        # Fit the model
        trainer.fit(self.model, train_dataloader)

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """
        Makes predictions on new data.
        """
        if self.model is None:
            raise RuntimeError("Model has not been trained yet. Call train() first.")

        # Create a dataloader for prediction
        prediction_dataset = self.create_dataset(data)
        predict_dataloader = prediction_dataset.to_dataloader(train=False, batch_size=64, num_workers=4)

        # Make predictions
        raw_predictions = self.model.predict(predict_dataloader)
        return raw_predictions[0].numpy() # Return predictions for the first batch

if __name__ == '__main__':
    # These would typically come from genesis.yaml or be determined by NAS
    mock_training_params = {
        "learning_rate": 0.01, "hidden_size": 32, "attention_head_size": 2,
        "dropout": 0.15, "hidden_continuous_size": 16,
    }

    predictor = UniversalPredictor(
        training_parameters=mock_training_params,
        max_prediction_length=20,
        max_encoder_length=60
    )

    # Create mock market data for training and prediction
    # Ensure there's enough data for at least one full sequence
    data_size = 200
    mock_data = pd.DataFrame({
        'time_idx': np.arange(data_size),
        'target': np.random.randn(data_size),
        'group': ['stock_A'] * data_size,
        'feature1': np.random.randn(data_size),
        'feature2': np.random.randn(data_size)
    })

    # Train the model
    print("Training the model...")
    predictor.train(mock_data)
    print("Training complete.")

    # Make predictions on the last sequence of the training data
    # The encoder data should be the last `max_encoder_length` time steps
    encoder_data = mock_data.iloc[-predictor.max_encoder_length:]

    print("\nMaking predictions...")
    predictions = predictor.predict(mock_data) # predict on the full data
    print("Predictions generated.")

    print(f"\nModel: {type(predictor.model)}")
    print(f"Prediction shape: {predictions.shape}")
