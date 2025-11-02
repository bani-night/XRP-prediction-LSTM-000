import unittest
import sys
import os

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apex.evolution.performance_dna import PerformanceDNA
from apex.evolution.knowledge_graph import KnowledgeGraph

class TestEvolutionComponents(unittest.TestCase):

    def test_performance_dna(self):
        """
        Tests that PerformanceDNA correctly tracks performance metrics.
        """
        perf_dna = PerformanceDNA(config={})

        perf_dna.update('BULLISH', {'is_correct': True, 'profit_loss_pct': 2.0})
        perf_dna.update('BEARISH', {'is_correct': False, 'profit_loss_pct': -1.0})
        perf_dna.update('BULLISH', {'is_correct': True, 'profit_loss_pct': 1.5})

        metrics = perf_dna.get_performance_metrics()

        self.assertAlmostEqual(metrics['win_rate'], 2/3)
        self.assertAlmostEqual(metrics['bullish_win_rate'], 1.0)
        self.assertAlmostEqual(metrics['bearish_win_rate'], 0.0)

    def test_knowledge_graph(self):
        """
        Tests that the KnowledgeGraph correctly builds associations.
        """
        kg = KnowledgeGraph(config={})

        kg.update_graph("VOLATILE", "phenotype_A", "BULLISH", True)
        kg.update_graph("VOLATILE", "phenotype_A", "BULLISH", True)
        kg.update_graph("STABLE", "phenotype_B", "BEARISH", True)

        volatile_associations = kg.get_strongest_associations("VOLATILE")
        self.assertEqual(volatile_associations["phenotype_A"], 2)

        success_associations = kg.get_strongest_associations("SUCCESS")
        self.assertEqual(success_associations["phenotype_A"], 2)
        self.assertEqual(success_associations["phenotype_B"], 1)

if __name__ == '__main__':
    unittest.main()
