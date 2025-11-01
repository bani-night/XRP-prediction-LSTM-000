import ccxt
import time

print("--- Starting network test ---")
start_time = time.time()

try:
    print("Attempting to initialize ccxt.binance()...")
    exchange = ccxt.binance()
    print("ccxt.binance() initialized successfully.")

    print("\nAttempting to load markets...")
    markets = exchange.load_markets()
    print("Markets loaded successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

end_time = time.time()
print(f"\n--- Test finished in {end_time - start_time:.2f} seconds ---")
