import time
import ccxt
import pandas as pd
import random
import numpy as np
from typing import Dict, Any, Generator

class MarketStream:
    """
    Handles data ingestion from live or mock sources, with realistic mock data generation.
    """

    def __init__(self, config: Dict[str, Any]):
        # ... (same as before)
        self.config = config
        self.primary_source = self.config.get('data_sources', {}).get('primary', 'mock')
        self.symbol = self.config.get('symbol', 'BTC/USDT')
        self.timeframe = self.config.get('timeframe', '1m')

        if self.primary_source != 'mock':
            self.exchange = getattr(ccxt, self.primary_source)()

    def get_live_data(self) -> Generator[pd.DataFrame, None, None]:
        if self.primary_source == 'mock':
            return self._mock_data_generator()
        else:
            return self._live_data_generator()

    def _mock_data_generator(self) -> Generator[pd.DataFrame, None, None]:
        """
        Generates a more realistic mock OHLCV dataset with trends, volatility, and NaNs.
        """
        price = 100.0
        trend = 0
        volatility = 0.1

        for i in range(500): # Generate a longer stream for better testing
            # --- Simulate Market Dynamics ---
            if i % 50 == 0: # Change trend periodically
                trend = random.uniform(-0.1, 0.1)
            if i % 100 == 0: # Change volatility periodically
                volatility = random.uniform(0.05, 0.3)

            # --- Generate Price Movement ---
            price_change = trend + random.uniform(-volatility, volatility)
            price += price_change

            # --- Create OHLCV data ---
            open_price = price - price_change
            high_price = max(price, open_price) + random.uniform(0, volatility)
            low_price = min(price, open_price) - random.uniform(0, volatility)
            close_price = price
            volume = random.uniform(10, 100)

            # --- Introduce occasional NaNs to test data handling ---
            if random.random() < 0.02: # 2% chance of a NaN value
                prop_to_nan = random.choice(['open', 'high', 'low', 'close'])
                if prop_to_nan == 'open': open_price = np.nan
                elif prop_to_nan == 'high': high_price = np.nan
                elif prop_to_nan == 'low': low_price = np.nan
                else: close_price = np.nan

            df = pd.DataFrame([{
                'timestamp': pd.Timestamp.now(), 'open': open_price, 'high': high_price,
                'low': low_price, 'close': close_price, 'volume': volume
            }])

            # For the purpose of the main loop, we yield a DataFrame of 100 rows
            # This is a simplification to match the expected output of the live feed
            mock_historical_data = pd.concat([df] * 100, ignore_index=True)
            yield mock_historical_data
            time.sleep(0.01) # Faster generation for testing


    def _live_data_generator(self) -> Generator[pd.DataFrame, None, None]:
        # ... (same as before)
        pass

if __name__ == '__main__':
    # ... (test code can be added here if needed)
    pass
