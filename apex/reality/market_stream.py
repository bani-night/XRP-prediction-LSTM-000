import time
import random
import pandas as pd
from typing import Dict, Any, Generator

class MarketStream:
    """
    Handles real-time data ingestion from market data sources.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the MarketStream with a configuration.

        Args:
            config: A dictionary containing data source configurations.
        """
        self.config = config
        self.primary_source = self.config.get('data_sources', {}).get('primary', 'mock')

    def get_live_data(self) -> Generator[pd.DataFrame, None, None]:
        """
        Yields live market data as a pandas DataFrame.

        This is a generator that will produce new data indefinitely.
        """
        if self.primary_source == 'mock':
            return self._mock_data_generator()
        else:
            # In a real implementation, you would connect to a live feed
            # using something like ccxt or python-binance.
            raise NotImplementedError(f"Data source '{self.primary_source}' is not yet implemented.")

    def _mock_data_generator(self) -> Generator[pd.DataFrame, None, None]:
        """
        A generator for producing mock market data.
        """
        base_price = 100.0
        while True:
            # Simulate a new tick of data
            price_change = random.uniform(-0.5, 0.5)
            base_price += price_change

            data = {
                'timestamp': [pd.Timestamp.now()],
                'open': [base_price - price_change],
                'high': [base_price + random.uniform(0, 0.2)],
                'low': [base_price - random.uniform(0, 0.2)],
                'close': [base_price],
                'volume': [random.uniform(10, 100)]
            }
            yield pd.DataFrame(data)
            time.sleep(1) # Simulate real-time data feed

if __name__ == '__main__':
    mock_config = {
        'data_sources': {
            'primary': 'mock'
        }
    }

    market_stream = MarketStream(config=mock_config)
    data_generator = market_stream.get_live_data()

    print("Starting mock market data stream...")
    print("Press Ctrl+C to stop.")

    try:
        for i, data_tick in enumerate(data_generator):
            print(f"\nTick {i + 1}:")
            print(data_tick.to_string(index=False))
            if i >= 4: # Stop after 5 ticks for the example
                break
    except KeyboardInterrupt:
        print("\nStream stopped.")
