import time
import ccxt
import pandas as pd
import random
from typing import Dict, Any, Generator

class MarketStream:
    """
    Handles real-time data ingestion from both live and mock sources.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.primary_source = self.config.get('data_sources', {}).get('primary', 'mock')
        self.symbol = self.config.get('symbol', 'BTC/USDT')
        self.timeframe = self.config.get('timeframe', '1m')

        if self.primary_source != 'mock':
            # Initialize the exchange only for live data sources
            self.exchange = getattr(ccxt, self.primary_source)()

    def get_live_data(self) -> Generator[pd.DataFrame, None, None]:
        """
        Yields market data as a pandas DataFrame.
        """
        if self.primary_source == 'mock':
            return self._mock_data_generator()
        else:
            return self._live_data_generator()

    def _mock_data_generator(self) -> Generator[pd.DataFrame, None, None]:
        """
        A generator for producing mock market data.
        """
        base_price = 100.0
        for _ in range(100): # Limit the mock data to 100 ticks for testing
            base_price += random.uniform(-0.5, 0.5)
            data = {
                'timestamp': [pd.Timestamp.now()],
                'open': [base_price - random.uniform(0.1, 0.5)],
                'high': [base_price + random.uniform(0, 0.2)],
                'low': [base_price - random.uniform(0, 0.2)],
                'close': [base_price],
                'volume': [random.uniform(10, 100)]
            }
            yield pd.DataFrame(data)
            time.sleep(0.1) # Faster for testing

    def _live_data_generator(self) -> Generator[pd.DataFrame, None, None]:
        """
        Yields live market data from the specified exchange.
        """
        while True:
            try:
                ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=100)
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                yield df
                time.sleep(self.exchange.rateLimit / 1000)
            except Exception as e:
                print(f"Error fetching live data: {e}")
                time.sleep(30)


if __name__ == '__main__':
    # --- Test Mock Data ---
    mock_config = {'data_sources': {'primary': 'mock'}}
    market_stream_mock = MarketStream(config=mock_config)
    mock_generator = market_stream_mock.get_live_data()
    print("--- Testing Mock Data Stream ---")
    for i, data_tick in enumerate(mock_generator):
        if i >= 4: break
        print(data_tick.tail(1).to_string(index=False))

    # --- Test Live Data (will fail in this environment, but shows the logic) ---
    live_config = {
        'data_sources': {'primary': 'binance'},
        'symbol': 'BTC/USDT', 'timeframe': '1m'
    }
    market_stream_live = MarketStream(config=live_config)
    print("\n--- Testing Live Data Stream (expecting failure) ---")
    try:
        live_generator = market_stream_live.get_live_data()
        next(live_generator)
    except Exception as e:
        print(f"Live data test failed as expected: {e}")
