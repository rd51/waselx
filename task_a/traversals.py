"""Graph traversal algorithms (BFS and DFS)."""

from collections import deque
from typing import List, Dict, Set, Tuple


def breadth_first_search(graph, start: str) -> Tuple[List[str], Dict[str, int]]:
    """
    Perform BFS traversal from start node.
    
    Returns:
        Tuple of (traversal order, distances from start)
    """
    if start not in graph.nodes:
        raise ValueError(f"Start node '{start}' not in graph")
    
    visited = set()
    queue = deque([start])
    visited.add(start)
    traversal_order = []
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    
    while queue:
        node = queue.popleft()
        traversal_order.append(node)
        
        for neighbor, _, _, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                distances[neighbor] = distances[node] + 1
    
    return traversal_order, distances


def depth_first_search(graph, start: str) -> Tuple[List[str], Dict[str, int]]:
    """
    Perform DFS traversal from start node (iterative).
    
    Returns:
        Tuple of (traversal order, discovery times)
    """
    if start not in graph.nodes:
        raise ValueError(f"Start node '{start}' not in graph")
    
    visited = set()
    stack = [start]
    traversal_order = []
    discovery_time = {}
    time_counter = [0]
    
    while stack:
        node = stack.pop()
        
        if node not in visited:
            visited.add(node)
            traversal_order.append(node)
            discovery_time[node] = time_counter[0]
            time_counter[0] += 1
            
            # Add neighbors to stack in reverse order (for correct DFS order)
            neighbors = sorted([n for n, _, _, _ in graph.get_neighbors(node)], reverse=True)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return traversal_order, discovery_time


def dfs_recursive(graph, start: str) -> Tuple[List[str], Dict[str, int]]:
    """
    Perform DFS traversal from start node (recursive).
    
    Returns:
        Tuple of (traversal order, discovery times)
    """
    if start not in graph.nodes:
        raise ValueError(f"Start node '{start}' not in graph")
    
    visited = set()
    traversal_order = []
    discovery_time = {}
    time_counter = [0]
    
    def dfs_helper(node):
        visited.add(node)
        traversal_order.append(node)
        discovery_time[node] = time_counter[0]
        time_counter[0] += 1
        
        for neighbor, _, _, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                dfs_helper(neighbor)
    
    dfs_helper(start)
    return traversal_order, discovery_time


def check_connectivity(graph) -> bool:
    """Check if graph is fully connected."""
    if not graph.nodes:
        return True
    
    traversal, _ = breadth_first_search(graph, graph.nodes[0])
    return len(traversal) == len(graph.nodes)
