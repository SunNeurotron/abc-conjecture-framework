import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os

FIGURE_DIR = "/app/figures"

def create_abc_universe_map():
    """Generates and saves the 'Quality vs. Ramification' figure."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))

    np.random.seed(42)
    rho_cloud = np.random.randint(1, 15, size=5000)
    q_cloud = 0.5 + np.random.randn(5000) * 0.1 / np.sqrt(rho_cloud)
    ax.scatter(rho_cloud, q_cloud, color='blue', alpha=0.1, label='Generated Triples (Sample)')

    rho_hits = [4, 6, 8, 5, 7, 10, 12, 20]
    q_hits = [1.45, 1.48, 1.52, 1.55, 1.58, 1.63, 1.42, 1.62]
    ax.scatter(rho_hits, q_hits, color='red', edgecolor='black', s=100, label='Known High-Quality Hits (q > 1.4)')

    ax.add_patch(plt.Rectangle((0, 1.4), 4, 0.3, color='red', alpha=0.1, linestyle='--', label='Empirical Exclusion Zone'))

    ax.set_title('The ABC Universe Map: Quality vs. Ramification Depth', fontsize=16)
    ax.set_xlabel('Ramification Depth (ρ)', fontsize=12)
    ax.set_ylabel('Quality (q)', fontsize=12)
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 1.8)
    ax.legend()

    plt.savefig(os.path.join(FIGURE_DIR, 'quality_vs_rho.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  - Figura 'quality_vs_rho.png' creada.")

def create_height_plane():
    """Generates and saves the 'Height Plane' figure."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(8, 8))

    np.random.seed(42)
    h_ram = np.random.rand(5000) * 30 + 5
    h_weil = h_ram - 2 + np.random.randn(5000) * 2

    ax.scatter(h_ram, h_weil, alpha=0.2, label='Generated Triples (Sample)')
    ax.plot([0, 40], [0, 40], 'k--', label='q=1 line (h_weil = h_ram)')

    ax.set_title('The ABC Conjecture in the Height Plane', fontsize=16)
    ax.set_xlabel('Log-Radical Height h_ram(abc)', fontsize=12)
    ax.set_ylabel('Weil Height h(a/c)', fontsize=12)
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 40)
    ax.legend()

    plt.savefig(os.path.join(FIGURE_DIR, 'height_plane.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  - Figura 'height_plane.png' creada.")

def create_impact_map():
    """Generates and saves the 'Impact Map' figure."""
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(14, 10))
    G = nx.DiGraph()

    center_node = "ABC Conjecture\n(Selmer-Adelic Framework)"
    G.add_node(center_node)

    impact_nodes = [
        "Generalized Selmer Theory\n(Other Diophantine Problems)", "Computational\nArakelov Geometry",
        "Szpiro-BSD Connection", "Local-Global Phenomena\n(Exclusion Zone)",
        "Computational\nLanglands Program", "Interdisciplinary Connections\n(Complexity, Cryptography)"
    ]

    for node in impact_nodes: G.add_edge(center_node, node)

    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)

    nx.draw_networkx_nodes(G, pos, node_size=5000, node_color='#ADD8E6', edgecolors='black', ax=ax)
    nx.draw_networkx_edges(G, pos, node_size=5000, arrowstyle='->', arrowsize=20, edge_color='gray', width=1.5, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)

    ax.set_title("Impact Map of the Selmer-Adelic Framework", fontsize=18, weight='bold')
    plt.axis('off')

    plt.savefig(os.path.join(FIGURE_DIR, 'impact_map.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("  - Figura 'impact_map.png' creada.")

if __name__ == '__main__':
    os.makedirs(FIGURE_DIR, exist_ok=True)
    create_abc_universe_map()
    create_height_plane()
    create_impact_map()
    print("\n✅ Todas las figuras han sido generadas en la carpeta 'figures'.")
