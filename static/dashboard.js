/**
 * WaselX Dashboard JavaScript
 * Interactive controls and API calls
 */

// API Base URL
const API_BASE = '/api';

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 WaselX Dashboard Initializing...');
    
    initializeDashboard();
    loadNetworkGraph();
    loadSortingBenchmark();
    loadSearchBenchmark();
    loadMSTInfo();
    updateStatus();
    
    // Auto-refresh status every 10 seconds
    setInterval(updateStatus, 10000);
});

/**
 * Initialize dashboard components
 */
function initializeDashboard() {
    console.log('✓ Dashboard initialized');
}

/**
 * Update network status
 */
function updateStatus() {
    fetch(`${API_BASE}/simulator-status`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const d = data.data;
                document.getElementById('total-nodes').textContent = d.total_nodes;
                document.getElementById('total-edges').textContent = d.total_edges;
                document.getElementById('blocked-routes').textContent = d.blocked_edges;
                document.getElementById('sim-active').textContent = (d.total_edges - d.blocked_edges * 2);
                document.getElementById('sim-blocked').textContent = d.blocked_edges;
            }
        })
        .catch(error => console.error('Error updating status:', error));
}

/**
 * Load and display network graph
 */
function loadNetworkGraph() {
    fetch(`${API_BASE}/graph`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const graph = JSON.parse(data.graph);
                Plotly.newPlot('network-graph', graph.data, graph.layout, {responsive: true});
                Plotly.newPlot('path-graph', graph.data, graph.layout, {responsive: true});
                Plotly.newPlot('simulator-graph', graph.data, graph.layout, {responsive: true});
            }
        })
        .catch(error => console.error('Error loading network graph:', error));
}

/**
 * Find shortest path
 */
function findPath() {
    const start = document.getElementById('path-start').value;
    const end = document.getElementById('path-end').value;
    const weight = document.getElementById('path-weight').value;
    
    if (!start || !end) {
        alert('Please select both start and end nodes');
        return;
    }
    
    if (start === end) {
        alert('Start and end nodes must be different');
        return;
    }
    
    const payload = {start, end, weight};
    
    fetch(`${API_BASE}/shortest-path`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const result = data.data;
            
            // Display results
            document.getElementById('result-path').textContent = result.path_labels.join(' → ');
            document.getElementById('result-distance').textContent = result.distance.toFixed(1);
            document.getElementById('result-time').textContent = result.time.toFixed(0);
            document.getElementById('result-cost').textContent = result.cost.toFixed(2);
            document.getElementById('path-result').style.display = 'block';
            
            // Display graph
            const graph = JSON.parse(result.graph);
            Plotly.newPlot('path-graph', graph.data, graph.layout, {responsive: true});
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error finding path:', error);
        alert('Error finding path');
    });
}

/**
 * Compare paths with all criteria
 */
function comparePaths() {
    const start = document.getElementById('path-start').value;
    const end = document.getElementById('path-end').value;
    
    if (!start || !end) {
        alert('Please select both start and end nodes');
        return;
    }
    
    if (start === end) {
        alert('Start and end nodes must be different');
        return;
    }
    
    const payload = {start, end};
    
    fetch(`${API_BASE}/compare-paths`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const result = data.data;
            
            // Display first path as example
            const firstPath = result.paths[0];
            document.getElementById('result-path').textContent = firstPath.path_labels.join(' → ');
            document.getElementById('result-distance').textContent = firstPath.distance.toFixed(1);
            document.getElementById('result-time').textContent = firstPath.time.toFixed(0);
            document.getElementById('result-cost').textContent = firstPath.cost.toFixed(2);
            document.getElementById('path-result').style.display = 'block';
            
            // Display all paths on graph
            const graph = JSON.parse(result.graph);
            Plotly.newPlot('path-graph', graph.data, graph.layout, {responsive: true});
            
            // Show comparison in console
            console.log('Path Comparison:');
            result.paths.forEach(p => {
                console.log(`  ${p.criterion}: ${p.value.toFixed(2)}`);
            });
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error comparing paths:', error);
        alert('Error comparing paths');
    });
}

/**
 * Load sorting benchmark
 */
function loadSortingBenchmark() {
    fetch(`${API_BASE}/sorting-benchmark`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const graph = JSON.parse(data.graph);
                Plotly.newPlot('sorting-graph', graph.data, graph.layout, {responsive: true});
            }
        })
        .catch(error => console.error('Error loading sorting benchmark:', error));
}

/**
 * Load search benchmark
 */
function loadSearchBenchmark() {
    fetch(`${API_BASE}/search-benchmark`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const results = data.data;
                let html = '';
                
                results.forEach(r => {
                    html += `
                        <tr>
                            <td><strong>${r.target}</strong></td>
                            <td>${r.linear_comparisons} comparisons</td>
                            <td>${r.binary_comparisons} comparisons</td>
                            <td><span class="badge bg-success">${r.improvement}</span></td>
                        </tr>
                    `;
                });
                
                document.getElementById('search-results').innerHTML = html;
            }
        })
        .catch(error => console.error('Error loading search benchmark:', error));
}

/**
 * Load MST information
 */
function loadMSTInfo() {
    fetch(`${API_BASE}/mst`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const d = data.data;
                let html = `
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Kruskal's Algorithm</h6>
                            <ul class="list-unstyled">
                                <li><strong>Edges:</strong> ${d.kruskal.edges}</li>
                                <li><strong>Total Cost:</strong> ${d.kruskal.cost.toFixed(2)} AED</li>
                                <li><strong>Sample Connections:</strong></li>
                                <li><small>${d.kruskal.connections.join(', ')}</small></li>
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <h6>Prim's Algorithm</h6>
                            <ul class="list-unstyled">
                                <li><strong>Edges:</strong> ${d.prim.edges}</li>
                                <li><strong>Total Cost:</strong> ${d.prim.cost.toFixed(2)} AED</li>
                                <li><strong>Sample Connections:</strong></li>
                                <li><small>${d.prim.connections.join(', ')}</small></li>
                            </ul>
                        </div>
                    </div>
                `;
                
                document.getElementById('mst-info').innerHTML = html;
            }
        })
        .catch(error => console.error('Error loading MST info:', error));
}

/**
 * Block route (simulate road closure)
 */
function blockRoute() {
    const from = document.getElementById('closure-from').value;
    const to = document.getElementById('closure-to').value;
    
    if (!from || !to) {
        alert('Please select both nodes');
        return;
    }
    
    if (from === to) {
        alert('Nodes must be different');
        return;
    }
    
    const payload = {from, to, action: 'block'};
    
    fetch(`${API_BASE}/road-closure`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('closure-status').textContent = data.data.message;
            document.getElementById('closure-result').style.display = 'block';
            
            // Reload graph
            setTimeout(() => loadNetworkGraph(), 500);
            updateStatus();
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error blocking route:', error);
        alert('Error blocking route');
    });
}

/**
 * Clear all road closures
 */
function clearClosures() {
    if (!confirm('Clear all blocked routes?')) {
        return;
    }
    
    // Note: In production, add clear-all endpoint
    alert('Closures cleared. (In production, this would call a clear-all endpoint)');
    
    document.getElementById('closure-from').value = '';
    document.getElementById('closure-to').value = '';
    document.getElementById('closure-result').style.display = 'none';
    
    loadNetworkGraph();
    updateStatus();
}

/**
 * Format number with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Show loading indicator
 */
function showLoading(elementId) {
    document.getElementById(elementId).innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    `;
}

/**
 * Show error message
 */
function showError(elementId, message) {
    document.getElementById(elementId).innerHTML = `
        <div class="alert alert-danger" role="alert">
            ${message}
        </div>
    `;
}

// Console logging
console.log('%c🚀 WaselX Dashboard Ready', 'color: #10B981; font-size: 16px; font-weight: bold;');
console.log('%c📊 Features:', 'color: #3B82F6; font-weight: bold;');
console.log('  ✓ Network Visualization');
console.log('  ✓ Path Finder (Dijkstra)');
console.log('  ✓ Sorting Benchmarks');
console.log('  ✓ Search Comparison');
console.log('  ✓ MST Algorithms');
console.log('  ✓ Road Closure Simulator');
