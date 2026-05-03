"""Minimum Spanning Tree algorithms (Prim and Kruskal)."""

from typing import List, Tuple, Set
import heapq


class UnionFind:
    """Union-Find (Disjoint Set Union) data structure for Kruskal's algorithm."""
    
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x: int) -> int:
        """Find the root parent of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """Union two sets. Returns True if union was successful."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True


def kruskals_algorithm(graph, weight: str = 'distance') -> Tuple[List[Tuple[str, str, float]], float]:
    """
    Find Minimum Spanning Tree using Kruskal's algorithm (greedy + Union-Find).
    
    Args:
        graph: Graph object
        weight: Weight type ('distance', 'time', or 'cost')
    
    Returns:
        Tuple of (MST edges, total weight)
    """
    edges = []
    
    # Collect all edges with their weights
    seen = set()
    for from_node in graph.nodes:
        for to_node, dist, time, cost in graph.get_neighbors(from_node):
            edge = tuple(sorted([from_node, to_node]))
            if edge not in seen:
                seen.add(edge)
                
                if weight == 'distance':
                    w = dist
                elif weight == 'time':
                    w = time
                else:  # 'cost'
                    w = cost
                
                edges.append((w, from_node, to_node))
    
    # Sort edges by weight
    edges.sort()
    
    # Kruskal's algorithm
    uf = UnionFind(graph.num_nodes)
    mst_edges = []
    total_weight = 0
    
    for weight_val, from_node, to_node in edges:
        from_idx = graph.node_index[from_node]
        to_idx = graph.node_index[to_node]
        
        if uf.union(from_idx, to_idx):
            mst_edges.append((from_node, to_node, weight_val))
            total_weight += weight_val
            
            if len(mst_edges) == graph.num_nodes - 1:
                break
    
    return mst_edges, total_weight


def prims_algorithm(graph, start: str, weight: str = 'distance') -> Tuple[List[Tuple[str, str, float]], float]:
    """
    Find Minimum Spanning Tree using Prim's algorithm (greedy + min-heap).
    
    Args:
        graph: Graph object
        start: Starting node for Prim's algorithm
        weight: Weight type ('distance', 'time', or 'cost')
    
    Returns:
        Tuple of (MST edges, total weight)
    """
    if start not in graph.nodes:
        raise ValueError(f"Start node '{start}' not in graph")
    
    visited = set()
    mst_edges = []
    total_weight = 0
    
    # Min heap: (weight, from_node, to_node)
    pq = []
    
    # Start from given node
    visited.add(start)
    
    # Add all edges from start node to heap
    for neighbor, dist, time, cost in graph.get_neighbors(start):
        if weight == 'distance':
            w = dist
        elif weight == 'time':
            w = time
        else:  # 'cost'
            w = cost
        
        heapq.heappush(pq, (w, start, neighbor))
    
    # Prim's algorithm
    while pq and len(visited) < graph.num_nodes:
        w, from_node, to_node = heapq.heappop(pq)
        
        if to_node in visited:
            continue
        
        visited.add(to_node)
        mst_edges.append((from_node, to_node, w))
        total_weight += w
        
        # Add all edges from newly visited node
        for neighbor, dist, time, cost in graph.get_neighbors(to_node):
            if neighbor not in visited:
                if weight == 'distance':
                    w = dist
                elif weight == 'time':
                    w = time
                else:  # 'cost'
                    w = cost
                
                heapq.heappush(pq, (w, to_node, neighbor))
    
    return mst_edges, total_weight
