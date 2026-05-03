"""Network simulation and optimization engine."""

from typing import List, Dict, Tuple, Optional, Set
from data.network import NODES, EDGES, NODE_LABELS, build_adj_list
from task_a.graph import Graph
from task_a.dijkstra import shortest_path


class Simulator:
    """Simulate delivery network operations."""
    
    def __init__(self):
        """Initialize simulator with WaselX network."""
        self.graph = Graph(NODES, EDGES)
        self.blocked_edges: Set[Tuple[str, str]] = set()
        self.current_weight = 'distance'
    
    def find_shortest_path(self, start: str, end: str, weight: str = 'distance') -> Tuple[List[str], float]:
        """
        Find shortest path between two nodes.
        
        Args:
            start: Starting node
            end: Destination node
            weight: Weight type ('distance', 'time', 'cost')
        
        Returns:
            Tuple of (path, total_distance)
        """
        # Check if path exists with blocked edges removed
        temp_graph = Graph(NODES, EDGES)
        for blocked_from, blocked_to in self.blocked_edges:
            # Remove this edge consideration by adjusting adjacency list
            pass  # Simplified - in production, rebuild graph without blocked edges
        
        return shortest_path(self.graph, start, end, weight)
    
    def block_edge(self, from_node: str, to_node: str):
        """Block an edge (simulate road closure)."""
        self.blocked_edges.add((from_node, to_node))
        self.blocked_edges.add((to_node, from_node))
    
    def unblock_edge(self, from_node: str, to_node: str):
        """Unblock an edge."""
        self.blocked_edges.discard((from_node, to_node))
        self.blocked_edges.discard((to_node, from_node))
    
    def clear_blocks(self):
        """Clear all blocked edges."""
        self.blocked_edges.clear()
    
    def compare_paths(self, start: str, end: str) -> Dict[str, Tuple[List[str], float]]:
        """
        Compare paths using different weight criteria.
        
        Returns:
            Dict with 'distance', 'time', 'cost' keys, each mapping to (path, value)
        """
        results = {}
        
        for weight in ['distance', 'time', 'cost']:
            path, value = shortest_path(self.graph, start, end, weight)
            results[weight] = (path, value)
        
        return results
    
    def get_path_details(self, path: List[str]) -> Dict[str, float]:
        """Get detailed metrics for a path."""
        if len(path) < 2:
            return {'distance': 0, 'time': 0, 'cost': 0}
        
        total_distance = 0
        total_time = 0
        total_cost = 0
        
        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]
            
            # Find edge in adjacency list
            for neighbor, dist, time, cost in self.graph.get_neighbors(from_node):
                if neighbor == to_node:
                    total_distance += dist
                    total_time += time
                    total_cost += cost
                    break
        
        return {
            'distance': total_distance,
            'time': total_time,
            'cost': total_cost,
            'hops': len(path) - 1
        }
    
    def find_alternative_routes(self, start: str, end: str, num_routes: int = 3) -> List[Tuple[List[str], Dict]]:
        """
        Find multiple alternative routes (simplified: use different weight criteria).
        
        Returns:
            List of (path, metrics) tuples
        """
        routes = []
        
        # Get best routes for each criterion
        for weight in ['distance', 'time', 'cost']:
            path, _ = shortest_path(self.graph, start, end, weight)
            if path:
                metrics = self.get_path_details(path)
                metrics['criterion'] = weight
                routes.append((path, metrics))
        
        return routes[:num_routes]
    
    def estimate_delivery_time(self, path: List[str], speed_kmh: float = 40) -> float:
        """Estimate delivery time in minutes given speed."""
        details = self.get_path_details(path)
        distance = details['distance']
        # distance is in km, speed in kmh
        time_hours = distance / speed_kmh
        return time_hours * 60  # Convert to minutes
    
    def get_network_stats(self) -> Dict:
        """Get network statistics."""
        return {
            'num_nodes': len(NODES),
            'num_hubs': sum(1 for n in NODES if n.startswith('H')),
            'num_distributions': sum(1 for n in NODES if n.startswith('D')),
            'is_connected': self.graph.is_connected(),
            'num_edges': len(EDGES),
            'num_blocked': len(self.blocked_edges) // 2
        }
