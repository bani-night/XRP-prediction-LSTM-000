from typing import Dict, Any
import pandas as pd
import random

class RealityValidator:
    """
    Validates predictions against real market outcomes by simulating trades.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.transaction_cost_pct = self.config.get('risk', {}).get('transaction_cost_pct', 0.001)

    def validate_prediction(self, prediction: Dict[str, Any], market_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Validates a prediction by simulating a trade on the market data.

        Args:
            prediction: A dictionary containing the prediction details (e.g., direction).
            market_data: A DataFrame with at least two rows of market data to simulate a trade.
        """
        if len(market_data) < 2:
            return {'is_correct': False, 'profit_loss_pct': 0, 'reason': 'Not enough data to validate.'}

        entry_price = market_data['close'].iloc[-2]
        exit_price = market_data['close'].iloc[-1]

        # Simulate trade based on prediction
        # For simplicity, we assume a 'BULLISH' prediction means we buy and hold for one tick.
        if prediction.get('direction') == 'BULLISH':
            profit_loss = (exit_price - entry_price) - (entry_price * self.transaction_cost_pct)
        elif prediction.get('direction') == 'BEARISH': # Assuming short sell
            profit_loss = (entry_price - exit_price) - (entry_price * self.transaction_cost_pct)
        else: # NEUTRAL or unknown
            profit_loss = 0

        profit_loss_pct = (profit_loss / entry_price) * 100
        is_correct = profit_loss > 0

        return {
            'is_correct': is_correct,
            'profit_loss_pct': profit_loss_pct,
        }

if __name__ == '__main__':
    mock_config = {
        'risk': {'transaction_cost_pct': 0.001}
    }

    validator = RealityValidator(config=mock_config)

    # Mock a bullish prediction and market data where the price goes up
    bullish_prediction = {'direction': 'BULLISH'}
    market_up_data = pd.DataFrame({'close': [100.0, 101.5]})

    bullish_result = validator.validate_prediction(bullish_prediction, market_up_data)
    print("Validation for a correct BULLISH prediction:")
    print(bullish_result)

    # Mock a bearish prediction and market data where the price goes down
    bearish_prediction = {'direction': 'BEARISH'}
    market_down_data = pd.DataFrame({'close': [100.0, 98.5]})

    bearish_result = validator.validate_prediction(bearish_prediction, market_down_data)
    print("\nValidation for a correct BEARISH prediction:")
    print(bearish_result)

    # Mock a bullish prediction where the price goes down
    market_down_data_for_bullish = pd.DataFrame({'close': [100.0, 99.0]})
    incorrect_bullish_result = validator.validate_prediction(bullish_prediction, market_down_data_for_bullish)
    print("\nValidation for an incorrect BULLISH prediction:")
    print(incorrect_bullish_result)
