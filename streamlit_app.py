"""Self-contained Streamlit frontend for the WaselX DSA project."""

from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data.network import EDGES, NODE_LABELS, NODES
from task_a.floyd_warshall import find_best_connected_hub
from task_a.mst import kruskals_algorithm, prims_algorithm
from task_d.searching import binary_search, linear_search
from task_d.sorting import bubble_sort, merge_sort, quick_sort
from task_e.simulator import Simulator
from utils.visualizer import NODE_COLORS, NODE_POSITIONS


st.set_page_config(
    page_title="WaselX - Delivery Network Optimization",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f6f8fb;
        background-image:
            linear-gradient(90deg, rgba(30, 64, 175, 0.045) 1px, transparent 1px),
            linear-gradient(rgba(15, 118, 110, 0.045) 1px, transparent 1px),
            linear-gradient(135deg, #f7fbff 0%, #fffaf0 48%, #f5fff8 100%);
        background-size: 34px 34px, 34px 34px, 100% 100%;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1240px;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #133f4b 58%, #184e43 100%);
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }
    h1, h2, h3 {
        letter-spacing: 0;
    }
    .wx-insight {
        border: 1px solid rgba(15, 23, 42, 0.14);
        border-left: 6px solid #0f766e;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.91);
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.07);
        margin: 0.85rem 0 1rem;
    }
    .wx-insight h4 {
        color: #0f172a;
        margin: 0 0 0.45rem;
    }
    .wx-insight ul {
        margin: 0.25rem 0 0 1.1rem;
        color: #334155;
    }
    .wx-insight li {
        margin: 0.2rem 0;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(15, 23, 42, 0.18);
        box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
        background: rgba(255, 255, 255, 0.9);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


BUSINESS_CONTEXT = {
    "daily_orders": 3500,
    "peak_orders": 6000,
    "riders": 200,
    "restaurant_partners": 1200,
    "retail_merchants": 300,
    "route_waste_pct": 23,
    "annual_excess_cost_aed": 1_200_000,
    "dispatch_delay_min": 8,
    "late_complaint_pct": 12,
    "lookup_seconds": 45,
    "csat": 3.2,
}


def get_simulator() -> Simulator:
    """Keep one simulator instance for the current Streamlit session."""
    if "simulator" not in st.session_state:
        st.session_state.simulator = Simulator()
    return st.session_state.simulator


def get_blocked_edges(simulator: Simulator) -> list[tuple[str, str]]:
    """Return each blocked undirected edge once."""
    blocked = []
    seen = set()
    for from_node, to_node in simulator.blocked_edges:
        edge = tuple(sorted((from_node, to_node)))
        if edge not in seen:
            seen.add(edge)
            blocked.append(edge)
    return sorted(blocked)


def format_aed(value: int | float) -> str:
    """Format AED values compactly for KPI cards."""
    if value >= 1_000_000:
        return f"AED {value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"AED {value / 1_000:.0f}K"
    return f"AED {value:,.0f}"


def render_kpis(cards: list[tuple[str, str, str, str]]) -> None:
    """Render KPI cards with native Streamlit components."""
    columns = st.columns(len(cards))
    for column, (label, value, note, _accent) in zip(columns, cards):
        with column:
            with st.container(border=True):
                st.metric(label, value)
                st.caption(note)


def render_insight(title: str, bullets: list[str], accent: str = "#0f766e") -> None:
    """Render a business insight panel."""
    with st.container(border=True):
        st.markdown(f"#### {title}")
        for bullet in bullets:
            st.markdown(f"- {bullet}")


def render_plot_box(title: str, fig, caption: str | None = None) -> None:
    """Render an outlined plot container for network topology or charts."""
    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.plotly_chart(fig, width="stretch")
        if caption:
            st.caption(caption)


def edge_trace(edges, color="#d3d3d3", width=1.5, name="Routes", dash=None):
    """Build a Plotly line trace for a collection of network edges."""
    edge_x = []
    edge_y = []

    for from_node, to_node, *_ in edges:
        x0, y0 = NODE_POSITIONS[from_node]
        x1, y1 = NODE_POSITIONS[to_node]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    return go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=width, color=color, dash=dash),
        hoverinfo="none",
        name=name,
    )


def create_network_graph(highlighted_paths=None, blocked_edges=None, highlighted_edges=None):
    """Create the WaselX delivery network as a Plotly figure."""
    highlighted_paths = highlighted_paths or []
    blocked_edges = blocked_edges or []
    highlighted_edges = highlighted_edges or []
    blocked_set = {tuple(sorted(edge)) for edge in blocked_edges}

    active_edges = [
        edge for edge in EDGES
        if tuple(sorted((edge[0], edge[1]))) not in blocked_set
    ]

    fig = go.Figure()
    fig.add_trace(edge_trace(active_edges))

    if blocked_edges:
        blocked_plot_edges = [(a, b, 0, 0, 0) for a, b in blocked_edges]
        fig.add_trace(
            edge_trace(
                blocked_plot_edges,
                color="#d62728",
                width=3,
                name="Blocked routes",
                dash="dash",
            )
        )

    for edges, color, width, name in highlighted_edges:
        fig.add_trace(
            edge_trace(
                [(from_node, to_node, 0, 0, 0) for from_node, to_node, *_ in edges],
                color=color,
                width=width,
                name=name,
            )
        )

    for path, color, label in highlighted_paths:
        path_x = []
        path_y = []
        for node in path:
            x, y = NODE_POSITIONS[node]
            path_x.append(x)
            path_y.append(y)

        fig.add_trace(
            go.Scatter(
                x=path_x,
                y=path_y,
                mode="lines+markers",
                line=dict(width=4, color=color),
                marker=dict(size=9),
                name=label,
                hovertemplate="<b>%{text}</b><extra></extra>",
                text=[NODE_LABELS[n] for n in path],
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[NODE_POSITIONS[node][0] for node in NODES],
            y=[NODE_POSITIONS[node][1] for node in NODES],
            mode="markers+text",
            marker=dict(
                size=13,
                color=[NODE_COLORS[node] for node in NODES],
                line=dict(color="black", width=2),
            ),
            text=NODES,
            textposition="bottom center",
            hovertext=[f"{node}<br>{NODE_LABELS[node]}" for node in NODES],
            hoverinfo="text",
            name="Nodes",
        )
    )

    fig.update_layout(
        title="WaselX Delivery Network",
        showlegend=True,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="white",
        height=600,
    )
    return fig


def get_simulator_status():
    """Return current network simulator status."""
    simulator = get_simulator()
    stats = simulator.get_network_stats()
    hub_nodes = [node for node in NODES if node.startswith("H")]
    best_hub, _ = find_best_connected_hub(simulator.graph, hub_nodes)

    return {
        "total_nodes": stats["num_nodes"],
        "hubs": stats["num_hubs"],
        "distribution_centers": stats["num_distributions"],
        "total_edges": stats["num_edges"],
        "network_connected": stats["is_connected"],
        "blocked_edges": stats["num_blocked"],
        "best_hub": best_hub,
        "best_hub_label": NODE_LABELS[best_hub],
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def find_shortest_path(start, end, weight):
    """Find a shortest path directly with the project simulator."""
    simulator = get_simulator()
    path, _ = simulator.find_shortest_path(start, end, weight=weight)

    if not path:
        return None

    details = simulator.get_path_details(path)
    fig = create_network_graph(
        highlighted_paths=[(path, "#ff6b6b", f"{start} to {end}")],
        blocked_edges=get_blocked_edges(simulator),
    )

    return {
        "path": path,
        "path_labels": [NODE_LABELS[node] for node in path],
        "distance": details.get("distance", 0),
        "time": details.get("time", 0),
        "cost": details.get("cost", 0),
        "hops": details.get("hops", 0),
        "fig": fig,
    }


def compare_all_paths(start, end):
    """Compare paths by distance, time, and cost."""
    simulator = get_simulator()
    paths = simulator.compare_paths(start, end)
    colors = ["#ff6b6b", "#4ecdc4", "#45b7d1"]
    results = []
    highlighted = []

    for index, (criterion, (path, value)) in enumerate(paths.items()):
        if not path:
            continue
        details = simulator.get_path_details(path)
        results.append(
            {
                "criterion": criterion,
                "value": value,
                "path": path,
                "path_labels": [NODE_LABELS[node] for node in path],
                "distance": details.get("distance", 0),
                "time": details.get("time", 0),
                "cost": details.get("cost", 0),
            }
        )
        highlighted.append((path, colors[index], f"{criterion.upper()}: {value:.1f}"))

    return {
        "paths": results,
        "fig": create_network_graph(
            highlighted_paths=highlighted,
            blocked_edges=get_blocked_edges(simulator),
        ),
    }


def get_mst_results():
    """Calculate MST results directly from the simulator graph."""
    simulator = get_simulator()
    kruskal_edges, kruskal_cost = kruskals_algorithm(simulator.graph, weight="cost")
    prim_edges, prim_cost = prims_algorithm(simulator.graph, "H1", weight="cost")

    return {
        "kruskal": {
            "edges": len(kruskal_edges),
            "cost": kruskal_cost,
            "connections": [f"{from_node}-{to_node}" for from_node, to_node, _ in kruskal_edges[:5]],
            "raw_edges": kruskal_edges,
        },
        "prim": {
            "edges": len(prim_edges),
            "cost": prim_cost,
            "connections": [f"{from_node}-{to_node}" for from_node, to_node, _ in prim_edges[:5]],
            "raw_edges": prim_edges,
        },
    }


def get_sorting_benchmark():
    """Build sorting benchmark data and chart."""
    rows = []
    sizes = [10, 50, 100, 200, 500]

    for size in sizes:
        arr = list(range(size, 0, -1))
        _, bubble_comps = bubble_sort(arr)
        _, merge_comps = merge_sort(arr)
        _, quick_comps = quick_sort(arr)
        rows.append(
            {
                "Size": size,
                "Bubble Sort": bubble_comps,
                "Merge Sort": merge_comps,
                "Quick Sort": quick_comps,
            }
        )

    benchmark_df = pd.DataFrame(rows)
    fig = px.line(
        benchmark_df,
        x="Size",
        y=["Bubble Sort", "Merge Sort", "Quick Sort"],
        title="Sorting Algorithm Performance Comparison",
        labels={"value": "Comparisons", "variable": "Algorithm"},
        markers=True,
    )
    fig.update_layout(height=420, template="plotly_white", hovermode="x unified")

    return {"fig": fig, "data": benchmark_df}


def get_search_benchmark():
    """Compare linear and binary search on a deterministic sorted array."""
    arr = [2, 3, 5, 8, 9, 12, 14, 15, 18, 21]
    targets = [3, 12, 21]
    results = []

    for target in targets:
        _, linear_comps = linear_search(arr, target)
        _, binary_comps = binary_search(arr, target)
        results.append(
            {
                "target": target,
                "linear_comparisons": linear_comps,
                "binary_comparisons": binary_comps,
                "improvement": f"{((linear_comps - binary_comps) / linear_comps * 100):.1f}%",
            }
        )

    return results


def block_route(from_node, to_node):
    """Block a route in the session simulator."""
    simulator = get_simulator()
    valid_edges = {tuple(sorted((edge[0], edge[1]))) for edge in EDGES}
    requested_edge = tuple(sorted((from_node, to_node)))

    if requested_edge not in valid_edges:
        return {
            "ok": False,
            "message": f"No direct route exists between {from_node} and {to_node}.",
        }

    simulator.block_edge(from_node, to_node)
    return {
        "ok": True,
        "message": f"Route {from_node}-{to_node} blocked.",
        "blocked_edges": len(get_blocked_edges(simulator)),
    }


def clear_route_blocks():
    """Clear all blocked route markers."""
    get_simulator().clear_blocks()


with st.container(border=True):
    st.caption("UAE last-mile delivery simulator")
    st.title("WaselX Delivery Network Optimization")
    st.markdown(
        f"""
        A self-contained DSA command center for route planning, dispatch prioritization,
        order lookup, network resilience, and executive business impact analysis across
        **{len(NODES)} operating nodes**.
        """
    )

render_kpis(
    [
        (
            "Daily Orders",
            f"{BUSINESS_CONTEXT['daily_orders']:,}",
            f"Peaks at {BUSINESS_CONTEXT['peak_orders']:,} during Ramadan/holidays",
            "#0f766e",
        ),
        (
            "Rider Fleet",
            f"{BUSINESS_CONTEXT['riders']}",
            "Bikes and cars across UAE delivery zones",
            "#2563eb",
        ),
        (
            "Route Waste",
            f"{BUSINESS_CONTEXT['route_waste_pct']}%",
            f"{format_aed(BUSINESS_CONTEXT['annual_excess_cost_aed'])}/year fuel and time impact",
            "#dc2626",
        ),
        (
            "Support Lookup",
            f"{BUSINESS_CONTEXT['lookup_seconds']} sec",
            f"Current CSAT baseline: {BUSINESS_CONTEXT['csat']}/5",
            "#b45309",
        ),
    ]
)

with st.sidebar:
    st.header("WaselX Console")
    st.success("Self-contained mode")
    st.caption("No external Flask API is required on Streamlit Cloud.")
    st.markdown(
        f"""
        **Business baseline**

        - {BUSINESS_CONTEXT['restaurant_partners']:,}+ restaurant partners
        - {BUSINESS_CONTEXT['retail_merchants']:,}+ retail merchants
        - {BUSINESS_CONTEXT['dispatch_delay_min']}-minute dispatch delay
        - {BUSINESS_CONTEXT['late_complaint_pct']}% late-delivery complaints
        """
    )
    st.divider()

    page = st.radio(
        "Select Section:",
        ["Network", "Path Finder", "Algorithms", "Simulator"],
        label_visibility="collapsed",
    )


if page == "Network":
    st.header("Network Topology")

    status = get_simulator_status()
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Nodes", status["total_nodes"])
    with col2:
        st.metric("Hubs", status["hubs"])
    with col3:
        st.metric("Distribution Pts", status["distribution_centers"])
    with col4:
        st.metric("Routes", status["total_edges"])
    with col5:
        st.metric("Status", "Online" if status["network_connected"] else "Offline")

    render_insight(
        "Network business insight",
        [
            f"WaselX currently loses {BUSINESS_CONTEXT['route_waste_pct']}% extra distance against optimal routing, creating {format_aed(BUSINESS_CONTEXT['annual_excess_cost_aed'])} in annual fuel and time exposure.",
            f"The graph captures {status['hubs']} hub nodes and {status['distribution_centers']} delivery zones, matching the operating map from the assignment brief.",
            f"{status['best_hub']} ({status['best_hub_label']}) is the strongest hub candidate for control-tower visibility and inter-hub coordination.",
        ],
        "#0f766e",
    )

    st.divider()
    render_plot_box(
        "Outlined Network Topology",
        create_network_graph(blocked_edges=get_blocked_edges(get_simulator())),
        "Hub nodes, delivery zones, route edges, and any simulated road closures are shown in one boxed topology view.",
    )

    st.markdown(
        """
        **Network Structure:**
        - **Blue nodes:** distribution hubs (H1-H7)
        - **Orange nodes:** distribution centers (D1-D8)
        - **Edges:** bidirectional routes with distance, time, and cost metrics
        """
    )
    st.markdown(
        f"**Best connected hub:** {status['best_hub']} - {status['best_hub_label']}  \n"
        f"**Last refreshed:** {status['timestamp']}"
    )


elif page == "Path Finder":
    st.header("Find Shortest Path")
    render_insight(
        "Path finder business insight",
        [
            "Dijkstra's algorithm is the right fit for real-time source-to-destination routing because each order needs one best route, not every possible route pair.",
            f"At {BUSINESS_CONTEXT['daily_orders']:,} daily orders, even small distance reductions compound into measurable rider utilization and SLA gains.",
            "Compare distance, time, and AED cost to show when the cheapest route is not the fastest route for VIP or express orders.",
        ],
        "#2563eb",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        start_node = st.selectbox("Start Node", NODES, key="path_start")
    with col2:
        end_node = st.selectbox("End Node", NODES, index=7, key="path_end")
    with col3:
        weight = st.selectbox(
            "Optimization Criteria",
            ["distance", "time", "cost"],
            format_func=lambda x: {
                "distance": "Shortest Distance",
                "time": "Fastest Time",
                "cost": "Lowest Cost",
            }[x],
        )

    col1, col2 = st.columns([1, 1])
    with col1:
        find_btn = st.button("Find Path", use_container_width=True)
    with col2:
        compare_btn = st.button("Compare All Criteria", use_container_width=True)

    st.divider()

    if find_btn:
        result = find_shortest_path(start_node, end_node, weight)
        if result:
            st.markdown(f"**Path:** {' -> '.join(result['path'])}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Distance", f"{result['distance']} km")
            with col2:
                st.metric("Time", f"{result['time']} min")
            with col3:
                st.metric("Cost", f"{result['cost']} AED")
            with col4:
                st.metric("Hops", result["hops"])
            render_plot_box(
                "Outlined Path Topology",
                result["fig"],
                "The selected route is highlighted inside the network box for clear evaluator walkthroughs.",
            )
        else:
            st.error(f"No path found from {start_node} to {end_node}.")

    if compare_btn:
        result = compare_all_paths(start_node, end_node)
        path_items = result["paths"]

        if path_items:
            st.markdown("### Multi-Criteria Comparison")
            comparison_data = [
                {
                    "Criteria": item["criterion"].capitalize(),
                    "Distance (km)": item["distance"],
                    "Time (min)": item["time"],
                    "Cost (AED)": item["cost"],
                    "Path": " -> ".join(item["path"]),
                }
                for item in path_items
            ]
            st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)
            render_plot_box(
                "Outlined Multi-Criteria Topology",
                result["fig"],
                "Distance, time, and cost routes are overlaid so operational trade-offs are visible.",
            )
        else:
            st.error(f"No comparable paths found from {start_node} to {end_node}.")


elif page == "Algorithms":
    st.header("Algorithm Performance Benchmarks")
    render_insight(
        "Algorithm business insight",
        [
            f"Priority-queue dispatch targets the current {BUSINESS_CONTEXT['dispatch_delay_min']}-minute batch delay and helps protect VIP same-hour orders.",
            f"Binary search and tree-based indexing address the {BUSINESS_CONTEXT['lookup_seconds']}-second support lookup pain point behind CSAT {BUSINESS_CONTEXT['csat']}/5.",
            "MST planning supports the assignment's fiber-tracking system by minimizing infrastructure cost across all operating nodes.",
        ],
        "#7c3aed",
    )

    tab1, tab2, tab3 = st.tabs(["Sorting", "Minimum Spanning Tree", "Searching"])

    with tab1:
        st.subheader("Sorting Algorithm Performance")
        benchmark = get_sorting_benchmark()
        st.markdown(
            """
            **Comparison:** Bubble Sort vs Merge Sort vs Quick Sort
            - **Variable:** array size vs number of comparisons
            - **Test case:** reversed delivery-route list
            """
        )
        render_plot_box(
            "Outlined Sorting Benchmark",
            benchmark["fig"],
            "Comparison counts show why quadratic sorting becomes costly as order manifests scale.",
        )

        size_100 = benchmark["data"][benchmark["data"]["Size"] == 100].iloc[0]
        results_df = pd.DataFrame(
            {
                "Algorithm": ["Bubble Sort", "Merge Sort", "Quick Sort"],
                "Comparisons at n=100": [
                    int(size_100["Bubble Sort"]),
                    int(size_100["Merge Sort"]),
                    int(size_100["Quick Sort"]),
                ],
                "Time Complexity": ["O(n^2)", "O(n log n)", "O(n log n) average"],
                "Best Case": ["O(n)", "O(n log n)", "O(n log n)"],
            }
        )
        st.dataframe(results_df, use_container_width=True)

    with tab2:
        st.subheader("Minimum Spanning Tree")
        mst = get_mst_results()
        kruskal = mst["kruskal"]
        prim = mst["prim"]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Kruskal's Algorithm**")
            st.metric("Edges", kruskal["edges"])
            st.metric("Total Cost (AED)", f"{kruskal['cost']:.2f}")
            st.markdown(f"**Connections:** {', '.join(kruskal['connections'])}")

        with col2:
            st.markdown("**Prim's Algorithm**")
            st.metric("Edges", prim["edges"])
            st.metric("Total Cost (AED)", f"{prim['cost']:.2f}")
            st.markdown(f"**Connections:** {', '.join(prim['connections'])}")

        st.divider()
        comparison = pd.DataFrame(
            {
                "Algorithm": ["Kruskal's", "Prim's"],
                "Edges": [kruskal["edges"], prim["edges"]],
                "Total Cost (AED)": [f"{kruskal['cost']:.2f}", f"{prim['cost']:.2f}"],
                "Approach": ["Greedy by edges", "Greedy by vertices"],
            }
        )
        st.dataframe(comparison, use_container_width=True)

        mst_fig = create_network_graph(
            highlighted_edges=[(kruskal["raw_edges"], "#7c3aed", 4, "Kruskal MST cable plan")]
        )
        render_plot_box(
            "Outlined MST Topology",
            mst_fig,
            "The highlighted backbone shows the minimum-cost tracking infrastructure plan.",
        )

    with tab3:
        st.subheader("Search Algorithm Performance")
        search = get_search_benchmark()
        st.markdown(
            """
            **Comparison:** Linear Search vs Binary Search
            - **Tested on:** sorted delivery-route list
            - **Metric:** number of comparisons needed
            """
        )

        search_df = pd.DataFrame(
            [
                {
                    "Target Value": item["target"],
                    "Linear Search": item["linear_comparisons"],
                    "Binary Search": item["binary_comparisons"],
                    "Improvement": item["improvement"],
                }
                for item in search
            ]
        )
        st.dataframe(search_df, use_container_width=True)

        fig = px.bar(
            search_df,
            x="Target Value",
            y=["Linear Search", "Binary Search"],
            title="Search Algorithm Comparison",
            labels={"value": "Comparisons", "variable": "Algorithm"},
            barmode="group",
        )
        render_plot_box(
            "Outlined Search Benchmark",
            fig,
            "The lookup benchmark connects directly to customer-support wait time reduction.",
        )

    mst_context = get_mst_results()
    context_fig = create_network_graph(
        highlighted_edges=[(mst_context["kruskal"]["raw_edges"], "#0f766e", 3, "Cost-efficient backbone")]
    )
    render_plot_box(
        "Outlined Algorithm Topology Context",
        context_fig,
        "This boxed topology keeps the network visible while reviewing algorithm outputs.",
    )


elif page == "Simulator":
    st.header("Road Closure Simulator")
    render_insight(
        "Simulator business insight",
        [
            "Road closures should trigger immediate rerouting, dispatcher alerts, and updated rider guidance before SLA windows are missed.",
            "The assignment brief frames this as operational resilience: management needs live road feeds, route recalculation, and exception handling.",
            f"Protecting peak-volume days matters most because WaselX can reach {BUSINESS_CONTEXT['peak_orders']:,} orders during Ramadan and national holidays.",
        ],
        "#dc2626",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        from_node = st.selectbox("Block Route From", NODES, key="sim_from")
    with col2:
        to_node = st.selectbox("To", NODES, index=7, key="sim_to")
    with col3:
        st.write("")
        st.write("")
        block_btn = st.button("Block Route", use_container_width=True)

    if block_btn:
        result = block_route(from_node, to_node)
        if result["ok"]:
            st.success(result["message"])
        else:
            st.warning(result["message"])

    st.divider()
    status = get_simulator_status()
    blocked_edges = get_blocked_edges(get_simulator())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Routes", status["total_edges"] - len(blocked_edges))
    with col2:
        st.metric("Blocked Routes", len(blocked_edges))
    with col3:
        st.metric("Network Status", "Online" if status["network_connected"] else "Degraded")

    if blocked_edges:
        st.markdown("**Blocked Routes:**")
        for from_node, to_node in blocked_edges:
            st.write(f"- {from_node}-{to_node}")

        if st.button("Clear All Blocks"):
            clear_route_blocks()
            st.rerun()

    st.divider()
    render_plot_box(
        "Outlined Simulator Topology",
        create_network_graph(blocked_edges=blocked_edges),
        "Blocked routes are boxed and shown as dashed red lines for clear incident-review demos.",
    )
    st.markdown("The network remains operational for demonstration purposes while blocked routes are highlighted.")


st.divider()
st.markdown(
    """
    **WaselX Delivery Network Optimization** | Data Structures & Algorithms Project
    - 27 algorithmic tasks implemented
    - Self-contained Streamlit Cloud deployment
    - Multi-criteria path optimization
    """
)
