"""Visualization utilities using matplotlib."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch


# Fixed 2D positions for all nodes (geographical layout)
NODE_POSITIONS = {
    # Dubai area (left side)
    "H1": (0, 3),      # Dubai Marina Hub
    "H2": (1, 3),      # Business Bay Hub
    "H3": (1, 2),      # Downtown Dubai Hub
    "H4": (0, 2),      # Dubai Creek Harbor Hub
    "H7": (2, 1),      # Dubai Investment Park Hub
    "D1": (0, 1),      # Al Barsha Distribution
    "D2": (1, 1),      # Karama Distribution
    "D3": (0, 4),      # Deira Distribution
    "D4": (2, 2),      # Bur Dubai Distribution
    "D8": (3, 0),      # Dubai South Distribution
    
    # Sharjah area (middle-top)
    "D5": (2, 4),      # Mirdif Distribution
    
    # Abu Dhabi area (right side)
    "H5": (4, 2),      # Dubai Hills Hub
    "H6": (5, 2),      # Arabian Ranches Hub
    "D6": (5, 0),      # Jumeirah Distribution
    "D7": (4, 0),      # The Palm Distribution
}

NODE_COLORS = {
    # Hub nodes in blue
    "H1": "#1f77b4", "H2": "#1f77b4", "H3": "#1f77b4", "H4": "#1f77b4",
    "H5": "#1f77b4", "H6": "#1f77b4", "H7": "#1f77b4",
    # Distribution nodes in orange
    "D1": "#ff7f0e", "D2": "#ff7f0e", "D3": "#ff7f0e", "D4": "#ff7f0e",
    "D5": "#ff7f0e", "D6": "#ff7f0e", "D7": "#ff7f0e", "D8": "#ff7f0e",
}


def draw_network(graph_edges, highlighted_paths=None, title="WaselX Network"):
    """
    Draw the WaselX delivery network with optional highlighted paths.
    
    Args:
        graph_edges (list): List of edge tuples (from_node, to_node, distance, time, cost)
        highlighted_paths (list, optional): List of (path, color, label) tuples where:
                                           - path is a list of nodes forming a route
                                           - color is the color to draw the path
                                           - label is the legend label for the path
        title (str): Title for the plot
    
    Returns:
        matplotlib.figure.Figure: The figure object (caller can save or show it)
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    
    # Draw all edges in light gray
    for from_node, to_node, distance, time, cost in graph_edges:
        x_values = [NODE_POSITIONS[from_node][0], NODE_POSITIONS[to_node][0]]
        y_values = [NODE_POSITIONS[from_node][1], NODE_POSITIONS[to_node][1]]
        ax.plot(x_values, y_values, color='#d3d3d3', linewidth=1.5, zorder=1)
    
    # Draw highlighted paths with arrows
    legend_elements = []
    if highlighted_paths:
        for path, color, label in highlighted_paths:
            # Draw edges for this path with arrows
            for i in range(len(path) - 1):
                from_node = path[i]
                to_node = path[i + 1]
                
                from_pos = NODE_POSITIONS[from_node]
                to_pos = NODE_POSITIONS[to_node]
                
                # Create arrow patch
                arrow = FancyArrowPatch(
                    from_pos, to_pos,
                    arrowstyle='-|>',
                    color=color,
                    linewidth=2.5,
                    mutation_scale=20,
                    zorder=3
                )
                ax.add_patch(arrow)
            
            # Add to legend
            legend_elements.append(mpatches.Patch(color=color, label=label))
    
    # Draw all nodes
    for node, pos in NODE_POSITIONS.items():
        ax.plot(pos[0], pos[1], 'o', markersize=15, color=NODE_COLORS[node], 
                zorder=4, markeredgecolor='black', markeredgewidth=1.5)
    
    # Add node labels
    for node, pos in NODE_POSITIONS.items():
        ax.text(pos[0], pos[1] - 0.35, node, ha='center', va='top', 
                fontsize=10, fontweight='bold', zorder=5)
    
    # Add legend if highlighted paths exist
    if legend_elements:
        # Add hub/distribution legend
        hub_patch = mpatches.Patch(color="#1f77b4", label="Hub Nodes")
        dist_patch = mpatches.Patch(color="#ff7f0e", label="Distribution Centers")
        legend_elements = [hub_patch, dist_patch] + legend_elements
        
        ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    # Configure plot
    ax.set_xlabel('Geographic Position (West → East)', fontsize=11)
    ax.set_ylabel('Geographic Position (South → North)', fontsize=11)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.2, linestyle='--')
    ax.set_aspect('equal')
    
    # Set axis limits with some padding
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 4.5)
    
    plt.tight_layout()
    return fig


def visualize_network(graph):
    """Visualize the delivery network graph."""
    pass


def plot_results(data):
    """Plot optimization results."""
    pass
