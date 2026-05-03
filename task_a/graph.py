"""Graph data structure implementation."""

from collections import defaultdict, deque
from typing import Dict, List, Tuple, Set


class Graph:
    """Undirected weighted graph for delivery network."""
    
    def __init__(self, nodes: List[str], edges: List[Tuple[str, str, float, float, float]]):
        """
        Initialize graph with nodes and edges.
        
        Args:
            nodes: List of node IDs
            edges: List of edge tuples (from, to, distance, time, cost)
        """
        self.nodes = nodes
        self.num_nodes = len(nodes)
        self.node_index = {node: i for i, node in enumerate(nodes)}
        
        # Adjacency list: {node: [(neighbor, distance, time, cost), ...]}
        self.adj_list = defaultdict(list)
        
        # Adjacency matrix: distance_matrix, time_matrix, cost_matrix
        self.distance_matrix = [[float('inf')] * self.num_nodes for _ in range(self.num_nodes)]
        self.time_matrix = [[float('inf')] * self.num_nodes for _ in range(self.num_nodes)]
        self.cost_matrix = [[float('inf')] * self.num_nodes for _ in range(self.num_nodes)]
        
        # Initialize diagonal to 0
        for i in range(self.num_nodes):
            self.distance_matrix[i][i] = 0
            self.time_matrix[i][i] = 0
            self.cost_matrix[i][i] = 0
        
        # Add edges (bidirectional)
        for from_node, to_node, distance, time, cost in edges:
            self.add_edge(from_node, to_node, distance, time, cost)
    
    def add_edge(self, from_node: str, to_node: str, distance: float, time: float, cost: float):
        """Add bidirectional edge to graph."""
        self.adj_list[from_node].append((to_node, distance, time, cost))
        self.adj_list[to_node].append((from_node, distance, time, cost))
        
        from_idx = self.node_index[from_node]
        to_idx = self.node_index[to_node]
        
        self.distance_matrix[from_idx][to_idx] = distance
        self.distance_matrix[to_idx][from_idx] = distance
        
        self.time_matrix[from_idx][to_idx] = time
        self.time_matrix[to_idx][from_idx] = time
        
        self.cost_matrix[from_idx][to_idx] = cost
        self.cost_matrix[to_idx][from_idx] = cost
    
    def get_neighbors(self, node: str) -> List[Tuple[str, float, float, float]]:
        """Get neighbors of a node with edge weights."""
        return self.adj_list.get(node, [])
    
    def is_connected(self) -> bool:
        """Check if graph is connected using BFS."""
        if not self.nodes:
            return True
        
        visited = set()
        queue = deque([self.nodes[0]])
        visited.add(self.nodes[0])
        
        while queue:
            node = queue.popleft()
            for neighbor, _, _, _ in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) == len(self.nodes)
    
    def __repr__(self) -> str:
        return f"Graph({self.num_nodes} nodes, {len(self.nodes)} edges)"
