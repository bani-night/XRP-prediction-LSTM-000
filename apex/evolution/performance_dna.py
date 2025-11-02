from typing import Dict, Any

class PerformanceDNA:
    """
    Encodes the performance characteristics of the prediction system over time.
    It tracks metrics to allow the system to learn from its past performance.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.total_predictions = 0
        self.correct_predictions = 0

        self.bullish_predictions = 0
        self.correct_bullish_predictions = 0

        self.bearish_predictions = 0
        self.correct_bearish_predictions = 0

        self.total_profit_loss = 0

    def update(self, prediction: str, validation_result: Dict[str, Any]):
        """
        Updates the performance DNA with the result of a new prediction.
        """
        self.total_predictions += 1

        if validation_result['is_correct']:
            self.correct_predictions += 1

        if prediction == 'BULLISH':
            self.bullish_predictions += 1
            if validation_result['is_correct']:
                self.correct_bullish_predictions += 1
        elif prediction == 'BEARISH':
            self.bearish_predictions += 1
            if validation_result['is_correct']:
                self.correct_bearish_predictions += 1

        self.total_profit_loss += validation_result.get('profit_loss_pct', 0)

    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Returns a dictionary of the current performance metrics.
        """
        win_rate = (self.correct_predictions / self.total_predictions) if self.total_predictions > 0 else 0
        bullish_win_rate = (self.correct_bullish_predictions / self.bullish_predictions) if self.bullish_predictions > 0 else 0
        bearish_win_rate = (self.correct_bearish_predictions / self.bearish_predictions) if self.bearish_predictions > 0 else 0

        # A simple profit factor calculation
        # Note: This is a simplification. A real profit factor would separate gross profits and gross losses.
        profit_factor = self.total_profit_loss / self.total_predictions if self.total_predictions > 0 else 0

        return {
            'win_rate': win_rate,
            'bullish_win_rate': bullish_win_rate,
            'bearish_win_rate': bearish_win_rate,
            'avg_profit_loss_pct': profit_factor
        }

if __name__ == '__main__':
    perf_dna = PerformanceDNA(config={})

    # Simulate some prediction results
    perf_dna.update('BULLISH', {'is_correct': True, 'profit_loss_pct': 1.5})
    perf_dna.update('BULLISH', {'is_correct': False, 'profit_loss_pct': -0.5})
    perf_dna.update('BEARISH', {'is_correct': True, 'profit_loss_pct': 2.0})
    perf_dna.update('BEARISH', {'is_correct': True, 'profit_loss_pct': 1.0})

    metrics = perf_dna.get_performance_metrics()

    print("--- Performance DNA Metrics ---")
    for key, value in metrics.items():
        print(f"  {key}: {value:.2%}")

    assert abs(metrics['win_rate'] - 0.75) < 1e-9
    assert abs(metrics['bullish_win_rate'] - 0.5) < 1e-9
    assert abs(metrics['bearish_win_rate'] - 1.0) < 1e-9
