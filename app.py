"""
WaselX Web Dashboard - Flask Application
Deployment-ready web interface for network optimization simulator
"""

import importlib
from functools import lru_cache
from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os


def _check_runtime_dependencies() -> None:
    """Fail fast with a clear install message when dependencies are missing."""
    required = ["flask", "flask_cors", "plotly"]
    for module_name in required:
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError:
            raise SystemExit(
                f"Missing dependency '{module_name}'. Install with: pip install -r requirements.txt"
            )


_check_runtime_dependencies()

# Import WaselX modules
from data.network import NODES, NODE_LABELS, EDGES, build_adj_list
from task_a.graph import Graph
from task_a.dijkstra import shortest_path
from task_a.floyd_warshall import floyd_warshall, find_best_connected_hub
from task_a.mst import kruskals_algorithm, prims_algorithm
from task_d.sorting import bubble_sort, merge_sort, quick_sort
from task_d.searching import linear_search, binary_search
from task_e.simulator import Simulator

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global simulator instance
simulator = Simulator()

# Create output directory
os.makedirs('outputs', exist_ok=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_network_graph(highlighted_paths=None):
    """Create Plotly network graph."""
    from utils.visualizer import NODE_POSITIONS, NODE_COLORS
    
    # Node positions
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    
    for node in NODES:
        x, y = NODE_POSITIONS[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node}<br>{NODE_LABELS[node]}")
        node_colors.append(NODE_COLORS[node])
    
    # Create edges
    edge_x = []
    edge_y = []
    
    for from_node, to_node, dist, time, cost in EDGES:
        x0, y0 = NODE_POSITIONS[from_node]
        x1, y1 = NODE_POSITIONS[to_node]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    
    # Create figure
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1.5, color='#d3d3d3'),
        hoverinfo='none',
        name='Routes'
    ))
    
    # Add highlighted paths
    if highlighted_paths:
        for path, color, label in highlighted_paths:
            path_x = []
            path_y = []
            
            for node in path:
                x, y = NODE_POSITIONS[node]
                path_x.append(x)
                path_y.append(y)
            
            fig.add_trace(go.Scatter(
                x=path_x, y=path_y,
                mode='lines+markers',
                line=dict(width=3, color=color),
                marker=dict(size=8),
                name=label,
                hovertemplate='<b>%{text}</b><extra></extra>',
                text=[NODE_LABELS[n] for n in path]
            ))
    
    # Add nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(
            size=12,
            color=node_colors,
            line=dict(color='black', width=2)
        ),
        text=NODES,
        textposition="bottom center",
        hovertext=node_text,
        hoverinfo='text',
        name='Nodes'
    ))
    
    # Update layout
    fig.update_layout(
        title='WaselX Delivery Network',
        showlegend=True,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        height=600
    )
    
    return fig


def create_sorting_benchmark():
    """Create sorting algorithm benchmark comparison."""
    sizes = [10, 50, 100, 200, 500]
    bubble_comps = []
    merge_comps = []
    quick_comps = []
    
    for size in sizes:
        arr = list(range(size, 0, -1))  # Worst case (reversed)
        
        _, b_comps = bubble_sort(arr)
        _, m_comps = merge_sort(arr)
        _, q_comps = quick_sort(arr)
        
        bubble_comps.append(b_comps)
        merge_comps.append(m_comps)
        quick_comps.append(q_comps)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=sizes, y=bubble_comps,
        mode='lines+markers',
        name='Bubble Sort',
        line=dict(color='#FF6B6B', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=sizes, y=merge_comps,
        mode='lines+markers',
        name='Merge Sort',
        line=dict(color='#4ECDC4', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=sizes, y=quick_comps,
        mode='lines+markers',
        name='Quick Sort',
        line=dict(color='#45B7D1', width=3)
    ))
    
    fig.update_layout(
        title='Sorting Algorithm Performance Comparison',
        xaxis_title='Array Size',
        yaxis_title='Number of Comparisons',
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    return fig


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main dashboard."""
    return render_template('index.html', 
                         nodes=NODES,
                         node_labels=NODE_LABELS)


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@lru_cache(maxsize=1)
def _plotly_js_bundle():
    """Return Plotly's local JavaScript bundle for offline dashboard rendering."""
    from plotly.offline import get_plotlyjs

    return get_plotlyjs()


@app.route('/plotly.min.js')
def plotly_js():
    """Serve Plotly locally so the dashboard works without CDN access."""
    return Response(_plotly_js_bundle(), mimetype='application/javascript')


@app.route('/api/network', methods=['GET'])
def api_network():
    """Get network overview."""
    stats = simulator.get_network_stats()
    
    hub_nodes = [n for n in NODES if n.startswith('H')]
    best_hub, _ = find_best_connected_hub(simulator.graph, hub_nodes)
    
    return jsonify({
        'status': 'success',
        'data': {
            'nodes': len(NODES),
            'hubs': stats['num_hubs'],
            'distributions': stats['num_distributions'],
            'edges': stats['num_edges'],
            'connected': stats['is_connected'],
            'best_hub': best_hub,
            'best_hub_label': NODE_LABELS[best_hub],
            'timestamp': datetime.now().isoformat()
        }
    })


@app.route('/api/graph', methods=['GET'])
def api_graph():
    """Get network graph visualization."""
    fig = create_network_graph()
    return jsonify({'status': 'success', 'graph': fig.to_json()})


@app.route('/api/shortest-path', methods=['POST'])
def api_shortest_path():
    """Find shortest path between two nodes."""
    data = request.json
    start = data.get('start')
    end = data.get('end')
    weight = data.get('weight', 'distance')
    
    if start not in NODES or end not in NODES:
        return jsonify({'status': 'error', 'message': 'Invalid nodes'}), 400
    
    try:
        path, distance = shortest_path(simulator.graph, start, end, weight=weight)
        
        if not path:
            return jsonify({
                'status': 'error',
                'message': f'No path found from {start} to {end}'
            }), 400
        
        # Get detailed metrics
        details = simulator.get_path_details(path)
        
        # Create visualization
        fig = create_network_graph(
            highlighted_paths=[(path, '#FF6B6B', f'{start} → {end}')]
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'path': path,
                'path_labels': [NODE_LABELS[n] for n in path],
                'distance': details.get('distance', 0),
                'time': details.get('time', 0),
                'cost': details.get('cost', 0),
                'hops': details.get('hops', 0),
                'graph': fig.to_json()
            }
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/compare-paths', methods=['POST'])
def api_compare_paths():
    """Compare paths using different weight criteria."""
    data = request.json
    start = data.get('start')
    end = data.get('end')
    
    if start not in NODES or end not in NODES:
        return jsonify({'status': 'error', 'message': 'Invalid nodes'}), 400
    
    try:
        paths = simulator.compare_paths(start, end)
        
        results = []
        highlighted = []
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        for i, (criterion, (path, value)) in enumerate(paths.items()):
            details = simulator.get_path_details(path)
            results.append({
                'criterion': criterion,
                'value': value,
                'path': path,
                'path_labels': [NODE_LABELS[n] for n in path],
                'distance': details.get('distance', 0),
                'time': details.get('time', 0),
                'cost': details.get('cost', 0)
            })
            highlighted.append((path, colors[i], f'{criterion.upper()}: {value:.1f}'))
        
        fig = create_network_graph(highlighted_paths=highlighted)
        
        return jsonify({
            'status': 'success',
            'data': {
                'paths': results,
                'graph': fig.to_json()
            }
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/mst', methods=['GET'])
def api_mst():
    """Calculate Minimum Spanning Tree."""
    try:
        kruskal_edges, kruskal_cost = kruskals_algorithm(simulator.graph, weight='cost')
        prim_edges, prim_cost = prims_algorithm(simulator.graph, 'H1', weight='cost')
        
        return jsonify({
            'status': 'success',
            'data': {
                'kruskal': {
                    'edges': len(kruskal_edges),
                    'cost': kruskal_cost,
                    'connections': [f'{f}-{t}' for f, t, _ in kruskal_edges[:5]]
                },
                'prim': {
                    'edges': len(prim_edges),
                    'cost': prim_cost,
                    'connections': [f'{f}-{t}' for f, t, _ in prim_edges[:5]]
                }
            }
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/sorting-benchmark', methods=['GET'])
def api_sorting_benchmark():
    """Get sorting algorithm benchmark."""
    try:
        fig = create_sorting_benchmark()
        return jsonify({'status': 'success', 'graph': fig.to_json()})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/road-closure', methods=['POST'])
def api_road_closure():
    """Simulate road closure."""
    data = request.json
    from_node = data.get('from')
    to_node = data.get('to')
    action = data.get('action', 'block')  # 'block' or 'unblock'
    
    if from_node not in NODES or to_node not in NODES:
        return jsonify({'status': 'error', 'message': 'Invalid nodes'}), 400
    
    try:
        if action == 'block':
            simulator.block_edge(from_node, to_node)
        else:
            simulator.unblock_edge(from_node, to_node)
        
        stats = simulator.get_network_stats()
        
        return jsonify({
            'status': 'success',
            'data': {
                'blocked_edges': stats['num_blocked'],
                'message': f'Edge {from_node}-{to_node} {action}ed'
            }
        })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/search-benchmark', methods=['GET'])
def api_search_benchmark():
    """Get search algorithm benchmark."""
    arr = [2, 3, 5, 8, 9, 12, 14, 15, 18, 21]
    targets = [3, 12, 21]
    
    results = []
    for target in targets:
        idx_l, comps_l = linear_search(arr, target)
        idx_b, comps_b = binary_search(arr, target)
        
        results.append({
            'target': target,
            'linear_comparisons': comps_l,
            'binary_comparisons': comps_b,
            'improvement': f'{((comps_l - comps_b) / comps_l * 100):.1f}%'
        })
    
    return jsonify({
        'status': 'success',
        'data': results
    })


@app.route('/api/simulator-status', methods=['GET'])
def api_simulator_status():
    """Get simulator status."""
    stats = simulator.get_network_stats()
    
    return jsonify({
        'status': 'success',
        'data': {
            'total_nodes': stats['num_nodes'],
            'hubs': stats['num_hubs'],
            'distribution_centers': stats['num_distributions'],
            'total_edges': stats['num_edges'],
            'network_connected': stats['is_connected'],
            'blocked_edges': stats['num_blocked'],
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
    })


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'status': 'error', 'message': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  WaselX - Delivery Network Optimization Dashboard")
    print("  Flask Web Server v1.0.0")
    print("="*70)
    print("\n[OK] Network initialized: 15 nodes, 24 edges")
    print("[OK] Simulators ready: Dijkstra, Floyd-Warshall, MST, Sorting, Searching")
    print("[OK] Dashboard available: http://localhost:5000")
    print("\nStarting Flask development server...\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )
