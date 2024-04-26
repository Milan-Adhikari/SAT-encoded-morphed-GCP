import networkx as nx
import random

def generate_ring_lattice():
    """Generate a regular ring lattice with 100 vertices and 8 nearest neighbors."""
    return nx.watts_strogatz_graph(100, 8, 0)

def generate_random_graph():
    """Generate a random graph with 100 vertices and 400 edges."""
    return nx.gnm_random_graph(100, 400)

def morph_graphs(G1, G2, p):
    """Create a p-morph of G1 and G2."""
    V = G1.nodes()
    E1 = set(G1.edges())
    E2 = set(G2.edges())
    
    # Edges common to both G1 and G2
    E_common = E1 & E2
    
    # Edges exclusive to G1
    E1_exclusive = list(E1 - E2)
    
    # Edges exclusive to G2
    E2_exclusive = list(E2 - E1)
    
    # Sample edges for the morph
    E_from_G1 = random.sample(E1_exclusive, int(p * len(E1_exclusive)))
    E_from_G2 = random.sample(E2_exclusive, int((1 - p) * len(E2_exclusive)))
    
    # Combine edges
    E_morph = list(E_common) + E_from_G1 + E_from_G2
    
    # Create the new graph with these edges
    G_morph = nx.Graph()
    G_morph.add_nodes_from(V)
    G_morph.add_edges_from(E_morph)
    
    return G_morph

def graph_to_dimacs_cnf(G, file_name):
    """Encode the graph coloring problem as a DIMACS CNF and save to a file."""
    num_vars = G.number_of_nodes()
    num_clauses = G.number_of_edges()
    clauses = []

    for edge in G.edges():
        u, v = edge
        clauses.append([-(u + 1), -(v + 1)])

    # Write to DIMACS CNF file
    with open(file_name, 'w') as file:
        file.write("c created by edge2cnf\n")
        file.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            file.write(" ".join(map(str, clause)) + " 0\n")

# Example usage
p_values = [0.01, 0.2]  # Morphing ratios
num_instances_per_p = 10  # Number of instances per morphing ratio

for p in p_values:
    for i in range(num_instances_per_p):
        G_ring_lattice = generate_ring_lattice()
        G_random = generate_random_graph()
        G_morph = morph_graphs(G_ring_lattice, G_random, p)
        
        # Filter out instances with chromatic number != 5
        chromatic_number = nx.algorithms.coloring.greedy_color(G_morph)
        if len(set(chromatic_number.values())) == 5:
            file_name = f"instance_p_{p}_num_{i}.cnf"
            graph_to_dimacs_cnf(G_morph, file_name)
            print(f"Instance {file_name} created with p={p}.")
