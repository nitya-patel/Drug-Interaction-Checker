"""
graph_engine.py (NetworkX + Pyvis)
------------------------------------
Builds an interactive drug interaction graph using NetworkX and Pyvis.
"""

import networkx as nx
from pyvis.network import Network


# Severity → color mapping
SEVERITY_COLORS = {
    "Mild": "#4CAF50",          # green
    "Moderate": "#FF9800",       # orange
    "Severe": "#F44336",         # red
    "Contraindicated": "#9C27B0" # purple
}

NODE_SAFE_COLOR = "#2979FF"     # blue for safe drugs
NODE_CONFLICT_COLOR = "#FF5252" # red-ish for drugs that have conflicts


def build_graph(drugs: list[str], conflicts: list[dict]) -> str:
    """
    Build an interactive Pyvis HTML graph of drug interactions.

    Args:
        drugs: list of drug name strings
        conflicts: list of conflict dicts {drug1, drug2, severity, description}

    Returns:
        HTML string (the full Pyvis graph page) to embed in Streamlit.
    """
    G = nx.Graph()

    # Determine which drugs have conflicts
    conflict_drugs = set()
    for c in conflicts:
        conflict_drugs.add(c["drug1"])
        conflict_drugs.add(c["drug2"])

    # Add nodes
    for drug in drugs:
        color = NODE_CONFLICT_COLOR if drug in conflict_drugs else NODE_SAFE_COLOR
        G.add_node(drug, color=color, title=f"{drug}\n{'⚠ Has interactions' if drug in conflict_drugs else '✓ No detected interactions'}", size=25)

    # Add edges
    for c in conflicts:
        edge_color = SEVERITY_COLORS.get(c["severity"], "#FF9800")
        G.add_edge(
            c["drug1"],
            c["drug2"],
            color=edge_color,
            title=f"Severity: {c['severity']}\n{c['description']}",
            width=3
        )

    # Build Pyvis network
    net = Network(
        height="500px",
        width="100%",
        bgcolor="#1a1a2e",
        font_color="#ffffff",
        directed=False
    )
    net.from_nx(G)

    # Physics options for smooth layout
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "stabilization": { "iterations": 200 },
        "barnesHut": {
          "gravitationalConstant": -5000,
          "springLength": 150,
          "springConstant": 0.05
        }
      },
      "nodes": {
        "font": { "size": 16, "color": "#ffffff" },
        "borderWidth": 2
      },
      "edges": {
        "smooth": { "type": "dynamic" },
        "font": { "size": 12, "color": "#cccccc" }
      }
    }
    """)

    # Return HTML string
    html = net.generate_html()
    return html
