import networkx as nx
from typing import Dict, Any

class KnowledgeGraph:
    """
    Learns and stores relationships between market patterns, strategies, and outcomes
    using a graph-based representation.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.graph = nx.Graph()

    def update_graph(self, market_regime: str, strategy_phenotype: str, prediction: str, is_correct: bool):
        """
        Updates the knowledge graph with new information from a prediction cycle.
        Nodes are added for regimes, strategies, and predictions, and edges are weighted by co-occurrence.
        """
        # Ensure nodes exist for each element
        self.graph.add_node(market_regime, type='regime')
        self.graph.add_node(strategy_phenotype, type='strategy')
        self.graph.add_node(prediction, type='prediction')

        # Add edges between the elements to represent their co-occurrence
        self._add_weighted_edge(market_regime, strategy_phenotype)
        self._add_weighted_edge(market_regime, prediction)
        self._add_weighted_edge(strategy_phenotype, prediction)

        # We can also add an 'outcome' node to represent success or failure
        outcome = "SUCCESS" if is_correct else "FAILURE"
        self.graph.add_node(outcome, type='outcome')
        self._add_weighted_edge(strategy_phenotype, outcome)

    def _add_weighted_edge(self, node1: str, node2: str):
        """
        Adds or increments the weight of an edge between two nodes.
        """
        if self.graph.has_edge(node1, node2):
            self.graph[node1][node2]['weight'] += 1
        else:
            self.graph.add_edge(node1, node2, weight=1)

    def get_strongest_associations(self, node: str) -> Dict[str, int]:
        """
        Returns the strongest associations for a given node, sorted by edge weight.
        """
        if node not in self.graph:
            return {}

        neighbors = sorted(
            self.graph.neighbors(node),
            key=lambda n: self.graph[node][n]['weight'],
            reverse=True
        )

        return {neighbor: self.graph[node][neighbor]['weight'] for neighbor in neighbors}

if __name__ == '__main__':
    kg = KnowledgeGraph(config={})

    # --- Simulate some data to build the graph ---
    kg.update_graph("VOLATILE", "rsi_True_macd_False", "BULLISH", True)
    kg.update_graph("VOLATILE", "rsi_True_macd_False", "BULLISH", True)
    kg.update_graph("VOLATILE", "rsi_False_macd_True", "BEARISH", False)
    kg.update_graph("STABLE", "rsi_True_macd_False", "BEARISH", True)

    # --- Test the graph's knowledge ---
    print("--- Knowledge Graph Associations ---")

    volatile_associations = kg.get_strongest_associations("VOLATILE")
    print(f"Associations for VOLATILE regime: {volatile_associations}")

    stable_associations = kg.get_strongest_associations("STABLE")
    print(f"Associations for STABLE regime: {stable_associations}")

    successful_strategy = kg.get_strongest_associations("SUCCESS")
    print(f"Associations for SUCCESS outcome: {successful_strategy}")

    assert "rsi_True_macd_False" in volatile_associations
    assert "rsi_True_macd_False" in successful_strategy
