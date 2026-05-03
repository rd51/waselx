"""Network data structures and utilities for WaselX."""

# List of all nodes in the network (15 total: 7 hubs + 8 distribution centers)
NODES = [
    "H1", "H2", "H3", "H4", "H5", "H6", "H7",  # Hubs
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"  # Distribution Centers
]

# Mapping of node IDs to their full names
NODE_LABELS = {
    "H1": "Dubai Marina Hub",
    "H2": "Business Bay Hub",
    "H3": "Downtown Dubai Hub",
    "H4": "Dubai Creek Harbor Hub",
    "H5": "Dubai Hills Hub",
    "H6": "Arabian Ranches Hub",
    "H7": "Dubai Investment Park Hub",
    "D1": "Al Barsha Distribution",
    "D2": "Karama Distribution",
    "D3": "Deira Distribution",
    "D4": "Bur Dubai Distribution",
    "D5": "Mirdif Distribution",
    "D6": "Jumeirah Distribution",
    "D7": "The Palm Distribution",
    "D8": "Dubai South Distribution",
}

# Network edges: (from_node, to_node, distance_km, time_min, cost_aed)
# All edges are bidirectional
EDGES = [
    # H1 connections
    ("H1", "H4", 5, 10, 3.5),
    ("H1", "D3", 4, 12, 3.0),
    ("H1", "D1", 8, 15, 5.5),
    ("H1", "H2", 10, 18, 7.0),
    
    # H4 connections
    ("H4", "D2", 6, 14, 4.0),
    ("H4", "H2", 7, 13, 5.0),
    
    # H2 connections
    ("H2", "D1", 3, 8, 2.5),
    ("H2", "H3", 9, 18, 6.0),
    
    # H3 connections
    ("H3", "D4", 12, 22, 8.0),
    ("H3", "H7", 15, 25, 10.0),
    ("H3", "D2", 8, 16, 5.5),
    
    # H7 connections
    ("H7", "D8", 4, 8, 3.0),
    ("H7", "D5", 10, 18, 7.0),
    
    # D1 connections
    ("D1", "D3", 5, 11, 3.5),
    ("D1", "D2", 6, 13, 4.0),
    
    # D2 connections
    ("D2", "D4", 10, 20, 7.0),
    
    # H5 connections
    ("H5", "D7", 6, 12, 4.0),
    ("H5", "H6", 14, 20, 9.0),
    ("H5", "D6", 12, 22, 8.0),
    
    # H6 connections
    ("H6", "D6", 8, 15, 5.5),
    ("H6", "D7", 10, 18, 7.0),
    
    # D6 connections
    ("D6", "D7", 7, 13, 5.0),
    
    # D4 connections
    ("D4", "D8", 18, 30, 12.0),
    
    # D5 connections
    ("D5", "D8", 8, 15, 5.5),
]


def build_adj_list(weight='distance'):
    """
    Build an adjacency list representation of the network.
    
    Args:
        weight (str): The weight to use for edges. Options:
                     'distance' (distance_km),
                     'time' (time_min),
                     'cost' (cost_aed)
    
    Returns:
        dict: Adjacency list where keys are node IDs and values are
              lists of (neighbor, weight) tuples.
    
    Raises:
        ValueError: If weight is not one of the valid options.
    """
    valid_weights = {'distance', 'time', 'cost'}
    
    if weight not in valid_weights:
        raise ValueError(f"weight must be one of {valid_weights}")
    
    adj_list = {node: [] for node in NODES}
    
    # Add edges (bidirectional)
    for from_node, to_node, distance, time, cost in EDGES:
        if weight == 'distance':
            edge_weight = distance
        elif weight == 'time':
            edge_weight = time
        else:  # 'cost'
            edge_weight = cost
        
        adj_list[from_node].append((to_node, edge_weight))
        adj_list[to_node].append((from_node, edge_weight))
    
    return adj_list


def load_network():
    """Load network data."""
    pass
