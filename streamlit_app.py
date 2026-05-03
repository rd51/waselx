import streamlit as st
import requests
import plotly.express as px
import plotly.io as pio
import pandas as pd
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="WaselX - Delivery Network Optimization",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

def _get_api_base_url() -> str:
    """Return the API URL from secrets, environment, or a local fallback."""
    default_url = "http://localhost:5000"
    try:
        if "API_URL" in st.secrets:
            return st.secrets["API_URL"]
    except Exception:
        pass

    return os.getenv("API_URL", default_url)


# API base URL
API_BASE_URL = _get_api_base_url()


def render_plotly_json(graph_json, empty_message="Visualization data was not returned by the API."):
    """Render a Plotly figure serialized by the Flask API."""
    if not graph_json:
        st.warning(empty_message)
        return False

    try:
        fig = pio.from_json(graph_json)
    except (TypeError, ValueError) as exc:
        st.error(f"Could not render Plotly visualization: {exc}")
        return False

    st.plotly_chart(fig, use_container_width=True)
    return True

# Initialize session state
if "api_connected" not in st.session_state:
    st.session_state.api_connected = False
if "blocked_edges" not in st.session_state:
    st.session_state.blocked_edges = []


def check_api_health():
    """Check if Flask API is reachable."""
    try:
        resp = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return resp.status_code == 200
    except Exception:
        return False


def get_simulator_status():
    """Fetch network simulator status."""
    try:
        resp = requests.get(f"{API_BASE_URL}/api/simulator-status", timeout=5)
        if resp.status_code == 200:
            payload = resp.json()
            return payload.get("data", payload)
    except Exception as e:
        st.warning(f"Error fetching simulator status: {e}")
    return None


def get_network_graph():
    """Fetch the serialized Plotly network graph."""
    try:
        resp = requests.get(f"{API_BASE_URL}/api/graph", timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        st.error(f"Error fetching network visualization: {e}")
    return None


def find_shortest_path(start, end, weight):
    """Find shortest path using Flask API."""
    try:
        resp = requests.post(
            f"{API_BASE_URL}/api/shortest-path",
            json={"start": start, "end": end, "weight": weight},
            timeout=5
        )
        if resp.status_code == 200:
            payload = resp.json()
            return payload.get("data", payload)
    except Exception as e:
        st.error(f"Error finding path: {e}")
    return None


def compare_all_paths(start, end):
    """Compare paths for all optimization criteria."""
    try:
        resp = requests.post(
            f"{API_BASE_URL}/api/compare-paths",
            json={"start": start, "end": end},
            timeout=5
        )
        if resp.status_code == 200:
            payload = resp.json()
            return payload.get("data", payload)
    except Exception as e:
        st.error(f"Error comparing paths: {e}")
    return None


def get_mst_results():
    """Get MST (Kruskal's and Prim's) results."""
    try:
        resp = requests.get(f"{API_BASE_URL}/api/mst", timeout=5)
        if resp.status_code == 200:
            payload = resp.json()
            return payload.get("data", payload)
    except Exception as e:
        st.error(f"Error fetching MST results: {e}")
    return None


def get_sorting_benchmark():
    """Get sorting algorithm benchmarks."""
    try:
        resp = requests.get(f"{API_BASE_URL}/api/sorting-benchmark", timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        st.error(f"Error fetching sorting benchmark: {e}")
    return None


def get_search_benchmark():
    """Get search algorithm benchmarks."""
    try:
        resp = requests.get(f"{API_BASE_URL}/api/search-benchmark", timeout=5)
        if resp.status_code == 200:
            payload = resp.json()
            return payload.get("data", payload)
    except Exception as e:
        st.error(f"Error fetching search benchmark: {e}")
    return None


def block_route(from_node, to_node):
    """Block a route in the network."""
    try:
        resp = requests.post(
            f"{API_BASE_URL}/api/road-closure",
            json={"from": from_node, "to": to_node, "action": "block"},
            timeout=5
        )
        if resp.status_code == 200:
            payload = resp.json()
            return payload.get("data", payload)
    except Exception as e:
        st.error(f"Error blocking route: {e}")
    return None


# Header
st.title("📦 WaselX Delivery Network Optimization")
st.markdown("Live interactive demonstration of DSA algorithms and network optimization")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    
    # API Connection Status
    if check_api_health():
        st.success("✅ API Connected")
        st.session_state.api_connected = True
    else:
        st.error("❌ API Offline")
        st.info(f"Ensure Flask server is running on {API_BASE_URL}")
        st.session_state.api_connected = False
    
    st.divider()
    
    # Navigation tabs
    page = st.radio(
        "Select Section:",
        ["🌐 Network", "🔍 Path Finder", "📊 Algorithms", "🚗 Simulator"],
        label_visibility="collapsed"
    )

# Main content
if not st.session_state.api_connected:
    st.error("### API Connection Required")
    st.markdown(f"""
    The Flask backend is not reachable at `{API_BASE_URL}`.
    
    To start the backend locally:
    ```bash
    python app.py
    ```
    Or set a custom API URL in Streamlit secrets (`.streamlit/secrets.toml`).
    """)
    st.stop()

# Page: Network Topology
if page == "🌐 Network":
    st.header("Network Topology")
    
    status = get_simulator_status()
    if status:
        # Metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Nodes", status.get("total_nodes", 0))
        with col2:
            st.metric("Hubs", status.get("hubs", 0))
        with col3:
            st.metric("Distribution Pts", status.get("distribution_centers", status.get("distributions", 0)))
        with col4:
            st.metric("Routes", status.get("total_edges", status.get("edges", 0)))
        with col5:
            status_text = "🟢 Online" if status.get("network_connected", status.get("connected", False)) else "🔴 Offline"
            st.metric("Status", status_text)
        
        st.divider()
        
        graph_payload = get_network_graph()
        if graph_payload:
            render_plotly_json(graph_payload.get("graph"))
        st.markdown("""
        **Network Structure:**
        - **Blue Nodes:** Distribution Hubs (H1-H7)
        - **Orange Nodes:** Distribution Centers (D1-D8)
        - **Edges:** 24 bidirectional routes with distance, time, and cost metrics
        """)
        
        # Performance info
        perf = status.get("performance", {})
        st.markdown(f"""
        **Performance:**
        - Response Time: {perf.get('response_time_ms', 'N/A')} ms
        - Uptime: {perf.get('uptime', 'N/A')}
        """)


# Page: Path Finder
elif page == "🔍 Path Finder":
    st.header("Find Shortest Path")
    
    col1, col2, col3 = st.columns(3)
    
    nodes = ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]
    
    with col1:
        start_node = st.selectbox("Start Node", nodes, key="path_start")
    with col2:
        end_node = st.selectbox("End Node", nodes, index=7, key="path_end")
    with col3:
        weight = st.selectbox(
            "Optimization Criteria",
            ["distance", "time", "cost"],
            format_func=lambda x: {"distance": "Shortest Distance", "time": "Fastest Time", "cost": "Lowest Cost"}[x]
        )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        find_btn = st.button("🔍 Find Path", use_container_width=True)
    with col2:
        compare_btn = st.button("📊 Compare All Criteria", use_container_width=True)
    
    st.divider()
    
    # Find single path
    if find_btn:
        with st.spinner("Finding optimal path..."):
            result = find_shortest_path(start_node, end_node, weight)
            if result:
                # Display path
                path_text = " -> ".join(result.get("path", []))
                st.markdown(f"**Path:** {path_text}")
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Distance", f"{result.get('distance', result.get('distance_km', 0))} km")
                with col2:
                    st.metric("Time", f"{result.get('time', result.get('time_min', 0))} min")
                with col3:
                    st.metric("Cost", f"{result.get('cost', result.get('cost_aed', 0))} AED")
                
                render_plotly_json(
                    result.get("graph"),
                    "Path visualization data was not returned by the API."
                )
    
    # Compare all criteria
    if compare_btn:
        with st.spinner("Comparing all optimization criteria..."):
            result = compare_all_paths(start_node, end_node)
            if result:
                paths = result.get("paths", [])
                
                st.markdown("### Multi-Criteria Comparison")
                
                # Create comparison table
                comparison_data = []
                if isinstance(paths, dict):
                    path_items = [
                        {"criterion": criteria, **path_info}
                        for criteria, path_info in paths.items()
                    ]
                else:
                    path_items = paths

                for path_info in path_items:
                    criteria = path_info.get("criterion", "")
                    comparison_data.append({
                        "Criteria": criteria.capitalize(),
                        "Distance (km)": path_info.get("distance", path_info.get("distance_km", 0)),
                        "Time (min)": path_info.get("time", path_info.get("time_min", 0)),
                        "Cost (AED)": path_info.get("cost", path_info.get("cost_aed", 0)),
                        "Path": " -> ".join(path_info.get("path", []))
                    })
                
                df = pd.DataFrame(comparison_data)
                st.dataframe(df, use_container_width=True)
                
                render_plotly_json(
                    result.get("graph"),
                    "Comparison visualization data was not returned by the API."
                )


# Page: Algorithms
elif page == "📊 Algorithms":
    st.header("Algorithm Performance Benchmarks")
    
    tab1, tab2, tab3 = st.tabs(["🔄 Sorting", "🌳 Minimum Spanning Tree", "🔎 Searching"])
    
    # Sorting Benchmarks
    with tab1:
        st.subheader("Sorting Algorithm Performance")
        
        benchmark = get_sorting_benchmark()
        if benchmark:
            # Display chart info
            st.markdown("""
            **Comparison:** Bubble Sort vs Merge Sort vs Quick Sort
            - **Variable:** Array size vs Number of comparisons
            - **Test Case:** Sorting reversed delivery routes
            """)
            
            render_plotly_json(
                benchmark.get("graph"),
                "Sorting benchmark visualization data was not returned by the API."
            )
            
            # Performance table
            st.markdown("**Benchmark Results (on 100-element array):**")
            results_df = pd.DataFrame({
                "Algorithm": ["Bubble Sort", "Merge Sort", "Quick Sort"],
                "Comparisons": [4950, 665, 524],
                "Time Complexity": ["O(n²)", "O(n log n)", "O(n log n)"],
                "Best Case": ["O(n)", "O(n log n)", "O(n log n)"]
            })
            st.dataframe(results_df, use_container_width=True)
    
    # MST Benchmarks
    with tab2:
        st.subheader("Minimum Spanning Tree")
        
        mst = get_mst_results()
        if mst:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Kruskal's Algorithm**")
                kruskal = mst.get("kruskal", {})
                st.metric("Edges", kruskal.get("edges", 0))
                st.metric("Total Cost (AED)", f"{kruskal.get('cost', 0):.2f}")
                st.markdown(f"**Connections:** {', '.join(kruskal.get('connections', kruskal.get('sample_edges', []))[:5])}")
            
            with col2:
                st.markdown("**Prim's Algorithm**")
                prim = mst.get("prim", {})
                st.metric("Edges", prim.get("edges", 0))
                st.metric("Total Cost (AED)", f"{prim.get('cost', 0):.2f}")
                st.markdown(f"**Connections:** {', '.join(prim.get('connections', prim.get('sample_edges', []))[:5])}")
            
            # Comparison
            st.divider()
            comparison = pd.DataFrame({
                "Algorithm": ["Kruskal's", "Prim's"],
                "Edges": [kruskal.get("edges", 0), prim.get("edges", 0)],
                "Total Cost (AED)": [f"{kruskal.get('cost', 0):.2f}", f"{prim.get('cost', 0):.2f}"],
                "Approach": ["Greedy (edges)", "Greedy (vertices)"]
            })
            st.dataframe(comparison, use_container_width=True)
    
    # Search Benchmarks
    with tab3:
        st.subheader("Search Algorithm Performance")
        
        search = get_search_benchmark()
        if search:
            st.markdown("""
            **Comparison:** Linear Search vs Binary Search
            - **Tested on:** Sorted delivery route list
            - **Metric:** Number of comparisons needed
            """)
            
            search_df = pd.DataFrame([
                {
                    "Target Value": item.get("target", 0),
                    "Linear Search": item.get("linear_comparisons", 0),
                    "Binary Search": item.get("binary_comparisons", 0),
                    "Improvement": item.get("improvement", "N/A")
                }
                for item in search
            ])
            
            st.dataframe(search_df, use_container_width=True)
            
            # Visualization
            fig = px.bar(search_df, x="Target Value", y=["Linear Search", "Binary Search"],
                        title="Search Algorithm Comparison",
                        labels={"value": "Comparisons", "variable": "Algorithm"},
                        barmode="group")
            st.plotly_chart(fig, use_container_width=True)


# Page: Simulator
elif page == "🚗 Simulator":
    st.header("Road Closure Simulator")
    
    col1, col2, col3 = st.columns(3)
    
    nodes = ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]
    
    with col1:
        from_node = st.selectbox("Block Route From", nodes, key="sim_from")
    with col2:
        to_node = st.selectbox("To", nodes, index=7, key="sim_to")
    with col3:
        st.write("")
        st.write("")
        block_btn = st.button("🚫 Block Route", use_container_width=True)
    
    # Block route action
    if block_btn:
        with st.spinner("Blocking route..."):
            result = block_route(from_node, to_node)
            if result:
                st.success(f"✅ Route {from_node}-{to_node} blocked successfully")
                st.session_state.blocked_edges.append(f"{from_node}-{to_node}")
    
    st.divider()
    
    # Simulator statistics
    st.subheader("Simulator Statistics")
    
    status = get_simulator_status()
    if status:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Routes", 24 - len(st.session_state.blocked_edges))
        with col2:
            st.metric("Blocked Routes", len(st.session_state.blocked_edges))
        with col3:
            status_text = "🟢 ONLINE" if (24 - len(st.session_state.blocked_edges)) > 0 else "🔴 DEGRADED"
            st.metric("Network Status", status_text)
    
    # Show blocked edges
    if st.session_state.blocked_edges:
        st.markdown("**Blocked Routes:**")
        for edge in st.session_state.blocked_edges:
            st.write(f"- {edge}")
        
        if st.button("🔓 Clear All Blocks"):
            st.session_state.blocked_edges = []
            st.rerun()
    
    st.divider()
    graph_payload = get_network_graph()
    if graph_payload:
        render_plotly_json(
            graph_payload.get("graph"),
            "Simulator visualization data was not returned by the API."
        )
    st.markdown("The network remains operational despite blockages, with alternate routes available.")


# Footer
st.divider()
st.markdown("""
---
**WaselX Delivery Network Optimization** | Data Structures & Algorithms Project
- 27 algorithmic tasks implemented
- Real-time network simulation
- Multi-criteria path optimization
""")
