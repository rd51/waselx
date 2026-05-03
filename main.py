"""Main entry point for WaselX delivery network optimization."""

import importlib
import sys
from data.network import NODES, NODE_LABELS, EDGES, build_adj_list
from task_a.graph import Graph
from task_a.dijkstra import shortest_path, dijkstra
from task_a.traversals import breadth_first_search, depth_first_search
from task_a.floyd_warshall import floyd_warshall, find_best_connected_hub, find_farthest_pair
from task_a.mst import kruskals_algorithm, prims_algorithm
from task_b.bst import BinarySearchTree
from task_b.avl import AVLTree
from task_c.linked_list import LinkedList
from task_c.circular_list import CircularLinkedList
from task_c.priority_queue import PriorityQueue
from task_c.stack import Stack
from task_d.sorting import bubble_sort, merge_sort, quick_sort
from task_d.searching import linear_search, binary_search
from task_e.simulator import Simulator
from utils.visualizer import draw_network


def _check_runtime_dependencies() -> None:
    """Fail fast with a clear install message when dependencies are missing."""
    required = ["numpy", "matplotlib", "plotly"]
    for module_name in required:
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError:
            raise SystemExit(
                f"Missing dependency '{module_name}'. Install with: pip install -r requirements.txt"
            )


_check_runtime_dependencies()


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def demo_graph_basics():
    """Task A - Q1, Q7: Graph basics and traversals."""
    print_section("TASK A - Q1 & Q7: Graph Basics & Traversals")
    
    # Build graph
    graph = Graph(NODES, EDGES)
    print(f"✓ Graph built: {graph}")
    print(f"✓ Connected: {graph.is_connected()}")
    
    # Q7: BFS and DFS from H3
    print("\nBFS Traversal from H3:")
    bfs_order, bfs_dist = breadth_first_search(graph, "H3")
    print(f"  Order: {' → '.join(bfs_order[:10])}...")
    print(f"  Hops from H3: {dict(list(bfs_dist.items())[:5])}")
    
    print("\nDFS Traversal from H3:")
    dfs_order, dfs_time = depth_first_search(graph, "H3")
    print(f"  Order: {' → '.join(dfs_order[:10])}...")


def demo_dijkstra():
    """Task A - Q2: Dijkstra's algorithm."""
    print_section("TASK A - Q2: Dijkstra's Shortest Path")
    
    graph = Graph(NODES, EDGES)
    
    # Q2: H1 → D1
    print("Finding shortest path: H1 → D1")
    path, distance = shortest_path(graph, "H1", "D1", weight='distance')
    print(f"  Path: {' → '.join(path)}")
    print(f"  Distance: {distance} km")
    print(f"  Nodes: {', '.join([NODE_LABELS[n] for n in path])}")


def demo_floyd_warshall():
    """Task A - Q3: Floyd-Warshall algorithm."""
    print_section("TASK A - Q3: Floyd-Warshall All-Pairs Shortest")
    
    graph = Graph(NODES, EDGES)
    hub_nodes = [n for n in NODES if n.startswith('H')]
    
    print(f"Analyzing {len(hub_nodes)} hub nodes: {', '.join(hub_nodes)}")
    
    # Best connected hub
    best_hub, total = find_best_connected_hub(graph, hub_nodes, weight='distance')
    print(f"  Best-connected hub: {best_hub} ({NODE_LABELS[best_hub]})")
    print(f"  Total distance to others: {total} km")
    
    # Farthest pair
    node1, node2, dist = find_farthest_pair(graph, weight='distance')
    print(f"  Farthest pair: {node1} ↔ {node2} ({dist} km)")


def demo_mst():
    """Task A - Q4: Minimum Spanning Tree."""
    print_section("TASK A - Q4: Minimum Spanning Tree (MST)")
    
    graph = Graph(NODES, EDGES)
    
    print("Kruskal's Algorithm:")
    kruskal_edges, kruskal_cost = kruskals_algorithm(graph, weight='cost')
    print(f"  MST edges: {len(kruskal_edges)}")
    print(f"  Total cost: {kruskal_cost} AED")
    print(f"  Sample edges: {kruskal_edges[:3]}")
    
    print("\nPrim's Algorithm (from H1):")
    prim_edges, prim_cost = prims_algorithm(graph, "H1", weight='cost')
    print(f"  MST edges: {len(prim_edges)}")
    print(f"  Total cost: {prim_cost} AED")


def demo_binary_trees():
    """Task B - Q8 & Q9: BST and AVL trees."""
    print_section("TASK B - Q8 & Q9: Binary Search Trees & AVL Trees")
    
    # Sample order IDs
    order_ids = [1067, 1234, 1045, 1089, 1012, 1156, 1078, 1098, 1042, 1087, 1101, 1129]
    
    print(f"Inserting {len(order_ids)} order IDs into trees...")
    
    # BST
    bst = BinarySearchTree()
    for order_id in order_ids:
        bst.insert(order_id)
    
    print(f"\nBST:")
    print(f"  Height: {bst.height()}")
    print(f"  In-order (sorted): {bst.inorder_traversal()[:5]}...")
    print(f"  Search 1067: {bst.search(1067)}")
    
    # AVL
    avl = AVLTree()
    for order_id in order_ids:
        avl.insert(order_id)
    
    print(f"\nAVL Tree:")
    print(f"  Height: {avl.height()}")
    print(f"  Rotations: {avl.rotation_count}")
    print(f"  In-order: {avl.inorder_traversal()[:5]}...")
    print(f"  More balanced: {avl.height() < bst.height()}")


def demo_linear_structures():
    """Task C - Q12-15: Linked Lists, Queues, Stacks."""
    print_section("TASK C - Q12-15: Linear Data Structures")
    
    # Linked List
    print("Singly Linked List (Route stops):")
    ll = LinkedList()
    stops = ["Marina", "Downtown", "Creek", "Business Bay", "Deira"]
    for stop in stops:
        ll.insert_at_tail(stop)
    print(f"  Route: {ll.to_list()}")
    print(f"  Size: {len(ll)}")
    
    # Circular List
    print("\nCircular Linked List (Rider rotation):")
    cll = CircularLinkedList()
    riders = ["Rider1", "Rider2", "Rider3", "Rider4"]
    for rider in riders:
        cll.insert(rider)
    print(f"  Riders: {cll.to_list()}")
    
    # Priority Queue
    print("\nPriority Queue (Order priorities):")
    pq = PriorityQueue()
    orders = [(1, "Order001"), (3, "Order002"), (1, "Order003"), (2, "Order004")]
    for priority, order in orders:
        pq.enqueue(order, priority)
    
    print(f"  Queue size: {len(pq)}")
    for _ in range(min(3, len(pq))):
        pri, order = pq.peek()
        print(f"  Next: {order} (priority {pri})")
        pq.dequeue()
    
    # Stack
    print("\nStack (Order lifecycle):")
    stack = Stack()
    statuses = ["Created", "Assigned", "InTransit", "Delivered"]
    for status in statuses:
        stack.push(status)
    print(f"  Status history: {stack.to_list()}")


def demo_sorting():
    """Task D - Q18: Sorting algorithms."""
    print_section("TASK D - Q18: Sorting & Comparison")
    
    orders = [15, 3, 21, 8, 9, 2, 18, 12, 5, 14]
    
    print(f"Original array: {orders}")
    
    sorted_bubble, comp_bubble = bubble_sort(orders)
    print(f"\nBubble Sort:")
    print(f"  Result: {sorted_bubble}")
    print(f"  Comparisons: {comp_bubble}")
    
    sorted_merge, comp_merge = merge_sort(orders)
    print(f"\nMerge Sort:")
    print(f"  Result: {sorted_merge}")
    print(f"  Comparisons: {comp_merge}")
    
    sorted_quick, comp_quick = quick_sort(orders)
    print(f"\nQuick Sort:")
    print(f"  Result: {sorted_quick}")
    print(f"  Comparisons: {comp_quick}")


def demo_searching():
    """Task D - Q19: Searching algorithms."""
    print_section("TASK D - Q19: Searching & Comparison")
    
    sorted_orders = [2, 3, 5, 8, 9, 12, 14, 15, 18, 21]
    target = 12
    
    print(f"Sorted array: {sorted_orders}")
    print(f"Searching for: {target}")
    
    idx_linear, comp_linear = linear_search(sorted_orders, target)
    print(f"\nLinear Search:")
    print(f"  Found at index: {idx_linear}")
    print(f"  Comparisons: {comp_linear}")
    
    idx_binary, comp_binary = binary_search(sorted_orders, target)
    print(f"\nBinary Search:")
    print(f"  Found at index: {idx_binary}")
    print(f"  Comparisons: {comp_binary}")


def demo_simulator():
    """Task E - Q27: Network simulator."""
    print_section("TASK E - Q27: Comprehensive Network Simulator")
    
    sim = Simulator()
    print(f"Network initialized:")
    print(f"  Total nodes: {sim.get_network_stats()['num_nodes']}")
    print(f"  Hubs: {sim.get_network_stats()['num_hubs']}")
    print(f"  Distribution centers: {sim.get_network_stats()['num_distributions']}")
    
    # Find optimal paths
    print(f"\nOptimal paths (H1 → D8):")
    paths = sim.compare_paths("H1", "D8")
    
    for criterion, (path, value) in paths.items():
        print(f"  {criterion.upper()}: {value} | Path: {' → '.join(path[:5])}...")
    
    # Simulate road closure
    print(f"\nSimulating road closure (H3-D4 blocked):")
    sim.block_edge("H3", "D4")
    print(f"  Blocked edges: {len(sim.blocked_edges) // 2}")


def demo_visualization():
    """Generate network visualization."""
    print_section("Generating Network Visualization")
    
    graph = Graph(NODES, EDGES)
    
    # Example path for visualization
    path1, _ = shortest_path(graph, "H1", "D8", weight='distance')
    path2, _ = shortest_path(graph, "H1", "D8", weight='time')
    
    highlighted = [
        (path1, '#FF6B6B', 'Shortest Distance'),
        (path2, '#4ECDC4', 'Fastest Time')
    ]
    
    fig = draw_network(EDGES, highlighted_paths=highlighted, title="WaselX Network - Path Optimization")
    
    # Save figure
    output_path = "waselx_network_visualization.png"
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Visualization saved: {output_path}")
    
    return fig


def main():
    """Run the WaselX application."""
    print("\n" + "="*70)
    print("  WASELX - Delivery Network Optimization")
    print("  48-Hour Group Project - Live Simulators")
    print("="*70)
    
    try:
        # Run all demos
        demo_graph_basics()
        demo_dijkstra()
        demo_floyd_warshall()
        demo_mst()
        demo_binary_trees()
        demo_linear_structures()
        demo_sorting()
        demo_searching()
        demo_simulator()
        demo_visualization()
        
        print_section("✓ ALL SIMULATORS COMPLETED SUCCESSFULLY")
        print("\nTo display visualization: plt.show() in Python REPL")
        print("Network graph saved as: waselx_network_visualization.png")
        
        return 0
    
    except Exception as e:
        print_section("❌ ERROR DURING EXECUTION")
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
