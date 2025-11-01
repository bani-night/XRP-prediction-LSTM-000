import sys
import os

print("--- Starting import test ---")

# Ensure the project root is on the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(f"Appended to sys.path: {os.path.dirname(os.path.abspath(__file__))}")

try:
    from main import main
    print("Successfully imported 'main' from main.py")
except Exception as e:
    print(f"An error occurred during import: {e}")
    import traceback
    traceback.print_exc()

print("--- Import test finished ---")
