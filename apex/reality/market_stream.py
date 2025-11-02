import time
import ccxt
import pandas as pd
import random
from typing import Dict, Any, Generator

class MarketStream:
    """
    Handles real-time data ingestion with robust error handling and retry logic.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.primary_source = self.config.get('data_sources', {}).get('primary', 'mock')
        self.symbol = self.config.get('symbol', 'BTC/USDT')
        self.timeframe = self.config.get('timeframe', '1m')

        if self.primary_source != 'mock':
            self.exchange = getattr(ccxt, self.primary_source)()

    def get_live_data(self) -> Generator[pd.DataFrame, None, None]:
        if self.primary_source == 'mock':
            return self.mock_data_generator()
        else:
            return self.live_data_generator()

    def mock_data_generator(self) -> Generator[pd.DataFrame, None, None]:
        # ... (same as before)
        base_price = 100.0
        for _ in range(100):
            base_price += random.uniform(-0.5, 0.5)
            data = {
                'timestamp': [pd.Timestamp.now()], 'open': [base_price - 0.1],
                'high': [base_price + 0.1], 'low': [base_price - 0.1],
                'close': [base_price], 'volume': [random.uniform(10, 100)]
            }
            yield pd.DataFrame(data)
            time.sleep(0.1)

    def live_data_generator(self) -> Generator[pd.DataFrame, None, None]:
        """
        Yields live market data with a robust retry mechanism.
        """
        max_retries = 5
        retry_delay = 5 # seconds

        while True:
            for attempt in range(max_retries):
                try:
                    ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=100)
                    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                    yield df
                    time.sleep(self.exchange.rateLimit / 1000)
                    break # Break the retry loop on success

                except (ccxt.RequestTimeout, ccxt.DDoSProtection, ccxt.ExchangeNotAvailable, ccxt.NetworkError) as e:
                    print(f"Network error: {e}. Retrying in {retry_delay} seconds (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(retry_delay)
                    retry_delay *= 2 # Exponential backoff

                except ccxt.AuthenticationError as e:
                    print(f"Authentication error: {e}. Please check your API keys. Stopping.")
                    return

                except Exception as e:
                    print(f"An unexpected error occurred: {e}. Retrying in 60 seconds...")
                    time.sleep(60)
            else: # If all retries fail
                print("Max retries reached. Stopping data stream.")
                return

if __name__ == '__main__':
    # ... (same as before)
    pass
