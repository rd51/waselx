"""Dijkstra's shortest path algorithm."""

import heapq
from typing import Dict, List, Tuple, Optional


def dijkstra(graph, start: str, weight: str = 'distance') -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Find shortest paths from start node to all other nodes using Dijkstra's algorithm.
    
    Args:
        graph: Graph object with adjacency list
        start: Starting node ID
        weight: Weight type ('distance', 'time', or 'cost')
    
    Returns:
        Tuple of (distances dict, predecessors dict)
    """
    if start not in graph.nodes:
        raise ValueError(f"Start node '{start}' not in graph")
    
    # Initialize distances and predecessors
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    predecessors = {node: None for node in graph.nodes}
    visited = set()
    
    # Min heap: (distance, node)
    pq = [(0, start)]
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        # If current distance is greater than stored, skip
        if current_dist > distances[current_node]:
            continue
        
        # Check all neighbors
        for neighbor, dist, time, cost in graph.get_neighbors(current_node):
            # Select weight based on parameter
            if weight == 'distance':
                edge_weight = dist
            elif weight == 'time':
                edge_weight = time
            else:  # 'cost'
                edge_weight = cost
            
            new_distance = distances[current_node] + edge_weight
            
            # Update if shorter path found
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))
    
    return distances, predecessors


def reconstruct_path(predecessors: Dict[str, Optional[str]], start: str, end: str) -> List[str]:
    """Reconstruct shortest path from start to end."""
    if predecessors[end] is None and start != end:
        return []  # No path exists
    
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    path.reverse()
    return path


def shortest_path(graph, start: str, end: str, weight: str = 'distance') -> Tuple[List[str], float]:
    """
    Find shortest path between two nodes.
    
    Returns:
        Tuple of (path as list of nodes, total distance)
    """
    distances, predecessors = dijkstra(graph, start, weight)
    path = reconstruct_path(predecessors, start, end)
    
    if not path or distances[end] == float('inf'):
        return [], float('inf')
    
    return path, distances[end]
