import matplotlib.pyplot as plt
import networkx as nx
import random

def generate_ring_lattice():
    """Generate a regular ring lattice with 10 vertices and 2 nearest neighbors."""
    return nx.watts_strogatz_graph(10, 2, 0)

def generate_random_graph():
    """Generate a random graph with 10 vertices and 15 edges."""
    return nx.gnm_random_graph(10, 15)

def morph_graphs(G1, G2, p):
    """Create a p-morph of G1 and G2."""
    E1 = set(G1.edges())
    E2 = set(G2.edges())
    E_common = E1 & E2  # Edges common to both graphs
    E1_exclusive = list(E1 - E2)  # Edges unique to G1
    E2_exclusive = list(E2 - E1)  # Edges unique to G2
    
    # Take a fraction of exclusive edges from each graph
    E_from_G1 = random.sample(E1_exclusive, int(p * len(E1_exclusive)))
    E_from_G2 = random.sample(E2_exclusive, int((1 - p) * len(E2_exclusive)))
    
    # Create the new graph by combining these edges
    E_morph = list(E_common) + E_from_G1 + E_from_G2
    
    G_morph = nx.Graph()
    G_morph.add_edges_from(E_morph)  # Add edges to the new graph
    
    return G_morph


def plot_graph(G):
    """Plot the graph."""
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='skyblue', edge_color='gray')
    plt.show()


G_ring_lattice = generate_ring_lattice()
plot_graph(G_ring_lattice)

G_random = generate_random_graph()
plot_graph(G_random)

G_morph = morph_graphs(G_ring_lattice, G_random, 0.1)
plot_graph(G_morph)