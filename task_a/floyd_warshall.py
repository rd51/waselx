"""Floyd-Warshall all-pairs shortest path algorithm."""

from typing import List, Tuple, Dict
import copy


def floyd_warshall(graph, weight: str = 'distance') -> Tuple[List[List[float]], List[List[int]]]:
    """
    Find shortest paths between all pairs of vertices using Floyd-Warshall algorithm.
    
    Args:
        graph: Graph object with adjacency matrix
        weight: Weight type ('distance', 'time', or 'cost')
    
    Returns:
        Tuple of (distance matrix, next hop matrix for path reconstruction)
    """
    n = graph.num_nodes
    
    # Select appropriate matrix
    if weight == 'distance':
        matrix = copy.deepcopy(graph.distance_matrix)
    elif weight == 'time':
        matrix = copy.deepcopy(graph.time_matrix)
    else:  # 'cost'
        matrix = copy.deepcopy(graph.cost_matrix)
    
    # Initialize next hop matrix for path reconstruction
    next_hop = [[-1] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and matrix[i][j] != float('inf'):
                next_hop[i][j] = j
    
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if matrix[i][k] + matrix[k][j] < matrix[i][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
                    next_hop[i][j] = next_hop[i][k]
    
    return matrix, next_hop


def reconstruct_path_fw(next_hop: List[List[int]], start_idx: int, end_idx: int, nodes: List[str]) -> List[str]:
    """Reconstruct path from Floyd-Warshall next hop matrix."""
    if next_hop[start_idx][end_idx] == -1:
        return []
    
    path = [nodes[start_idx]]
    current = start_idx
    
    while current != end_idx:
        current = next_hop[current][end_idx]
        path.append(nodes[current])
    
    return path


def all_pairs_shortest_paths(graph, weight: str = 'distance') -> Dict[Tuple[str, str], float]:
    """
    Get all pairs shortest paths as a dictionary.
    
    Returns:
        Dictionary mapping (from_node, to_node) to shortest distance
    """
    dist_matrix, _ = floyd_warshall(graph, weight)
    
    result = {}
    for i, from_node in enumerate(graph.nodes):
        for j, to_node in enumerate(graph.nodes):
            result[(from_node, to_node)] = dist_matrix[i][j]
    
    return result


def find_farthest_pair(graph, weight: str = 'distance') -> Tuple[str, str, float]:
    """Find the pair of nodes with maximum shortest distance (diameter)."""
    dist_matrix, _ = floyd_warshall(graph, weight)
    
    max_dist = -1
    farthest_pair = (None, None)
    
    for i, from_node in enumerate(graph.nodes):
        for j, to_node in enumerate(graph.nodes):
            if i != j and dist_matrix[i][j] != float('inf'):
                if dist_matrix[i][j] > max_dist:
                    max_dist = dist_matrix[i][j]
                    farthest_pair = (from_node, to_node)
    
    if max_dist == -1:
        # No connected pair found, return zeros
        return graph.nodes[0], graph.nodes[1], 0
    
    return farthest_pair[0], farthest_pair[1], max_dist


def find_best_connected_hub(graph, hub_nodes: List[str], weight: str = 'distance') -> Tuple[str, float]:
    """Find hub with minimum total distance to all other hubs."""
    dist_matrix, _ = floyd_warshall(graph, weight)
    
    best_hub = hub_nodes[0]
    min_total = float('inf')
    
    for hub in hub_nodes:
        hub_idx = graph.node_index[hub]
        total = 0
        valid_count = 0
        
        for other_hub in hub_nodes:
            if other_hub != hub:
                other_idx = graph.node_index[other_hub]
                dist = dist_matrix[hub_idx][other_idx]
                
                # Only count reachable hubs
                if dist != float('inf'):
                    total += dist
                    valid_count += 1
        
        # Prefer hubs that can reach more hubs
        if valid_count > 0:
            avg_dist = total / valid_count
            if avg_dist < min_total or (avg_dist == min_total and valid_count > 0):
                min_total = avg_dist
                best_hub = hub
    
    return best_hub, min_total
