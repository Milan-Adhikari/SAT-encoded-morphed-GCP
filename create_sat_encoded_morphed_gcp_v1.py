import networkx as nx
import random

def generate_graph(num_vertices, edge_prob):
    """Generate a random graph."""
    return nx.gnp_random_graph(num_vertices, edge_prob)

def morph_graph(G, num_morphs):
    """Morph the graph by randomly adding edges."""
    for _ in range(num_morphs):
        u, v = random.sample(range(G.number_of_nodes()), 2)
        G.add_edge(u, v)

def graph_to_dimacs_cnf(G, num_colors, file_name):
    """Encode the graph coloring problem as a DIMACS CNF and save to a file."""
    clauses = []
    num_vars = num_colors * G.number_of_nodes()
    for node in G.nodes():
        # Each node must be one of the possible colors
        clauses.append([num_colors*node + i + 1 for i in range(num_colors)])

    for edge in G.edges():
        u, v = edge
        for color in range(num_colors):
            # Adjacent nodes cannot have the same color
            clauses.append([-(num_colors*u + color + 1), -(num_colors*v + color + 1)])

    # Write to DIMACS CNF file
    with open(file_name, 'w') as file:
        file.write("c created by edge2cnf\n")
        file.write(f"p cnf {num_vars} {len(clauses)}\n")
        for clause in clauses:
            file.write(" ".join(map(str, clause)) + " 0\n")

# Example usage:
num_vertices = 10  # Number of vertices in the graph
edge_prob = 0.5    # Probability of an edge being added between two vertices
num_morphs = 5     # Number of additional edges to add randomly
num_colors = 3     # Number of colors
file_name = 'output.cnf'  # Output file name

G = generate_graph(num_vertices, edge_prob)
morph_graph(G, num_morphs)
graph_to_dimacs_cnf(G, num_colors, file_name)
print(f"CNF file {file_name} created.")
