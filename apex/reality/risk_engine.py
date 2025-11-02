from typing import Dict, Any
import pandas as pd
import numpy as np

class RiskEngine:
    """
    Applies risk management rules to trading signals and portfolio state.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def manage_risk(self, df: pd.DataFrame, position: pd.Series, genome: Dict[str, Any]) -> pd.Series:
        """
        Applies stop-loss and take-profit rules to the trading positions.
        """
        # Identify trades (where position changes from 0 to 1)
        entry_signals = (position == 1) & (position.shift(1).fillna(0) == 0)

        # Get entry prices and forward-fill them for the duration of the trade
        entry_prices = df['close'].where(entry_signals).ffill()

        # --- Calculate Exit Prices ---
        stop_loss_prices = entry_prices * (1 - genome['stop_loss_pct'])
        take_profit_prices = entry_prices * (1 + genome['take_profit_pct'])

        # --- Generate Exit Signals ---
        stop_loss_triggered = df['low'] < stop_loss_prices
        take_profit_triggered = df['high'] > take_profit_prices

        # Combine all exit signals
        exit_signals = stop_loss_triggered | take_profit_triggered

        # When an exit is triggered, we need to find the start of that trade
        # and set the position to 0 from that point until the next trade starts.
        # This is complex to do in a purely vectorized way without iteration.
        # For this implementation, we will use a simplified approach:
        # Once an exit signal is hit, we exit and stay out until the next buy signal.

        # Create a signal to flip position to 0
        position[exit_signals] = 0

        # Forward-fill the state
        position.ffill(inplace=True)

        return position.astype(int)

if __name__ == '__main__':
    pass
