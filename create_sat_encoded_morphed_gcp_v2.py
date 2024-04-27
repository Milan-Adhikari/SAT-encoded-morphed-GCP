from typing import List
import networkx as nx
import random
import os

def generate_ring_lattice(num_vertices:int = 100, num_neighbors:int = 8):
    """Generate a regular ring lattice with {num_vertices} vertices and {num_neighbours} nearest neighbors."""
    return nx.watts_strogatz_graph(num_vertices, num_neighbors, 0)

def generate_random_graph(num_vertices:int = 100, num_edges:int = 400):
    """Generate a random graph with {num_vertices} vertices and {num_edges} edges."""
    return nx.gnm_random_graph(num_vertices, num_edges)

def morph_graphs(G1 : nx.Graph, G2: nx.Graph, p: float):
    """Create a p-morph of G1 and G2."""
    V = set(G1.nodes())  # Set of vertices in G1
    E1 = set(G1.edges())  # Set of edges in G1
    E2 = set(G2.edges())  # Set of edges in G2

    E_common = E1 & E2  # Edges common to both G1 and G2
    E1_exclusive = list(E1 - E2)  # Edges exclusive to G1
    E2_exclusive = list(E2 - E1)  # Edges exclusive to G2
    
    # Sample edges for the morph
    E_from_G1 = random.sample(E1_exclusive, int(p * len(E1_exclusive)))
    E_from_G2 = random.sample(E2_exclusive, int((1 - p) * len(E2_exclusive)))
    
    # Combine edges
    E_morph = list(E_common) + E_from_G1 + E_from_G2
    
    # Create the new graph with these edges and vertices
    G_morph = nx.Graph()  # Create an empty graph
    G_morph.add_nodes_from(V)  # Add the vertices
    G_morph.add_edges_from(E_morph)  # Add the edges
    
    return G_morph

def graph_to_dimacs_cnf(G: nx.Graph, file_name: str, num_colors: int):
    """Encode the graph coloring problem as a DIMACS CNF and save to a file."""
    num_vars = G.number_of_nodes() * num_colors  # Each node can be colored with num_colors
    clauses = []  # List to store the clauses

    # we loop through all the nodes 
    for node in G.nodes():
        # we loop through all the colors
        for i in range(1, num_colors + 1):
            for j in range(i + 1, num_colors + 1):
                # Node cannot have two different colors, so we add a clause with negation of the two colors
                clauses.append([-(node * num_colors + i), -(node * num_colors + j)])
        # At least one color must be assigned to the node
        clauses.append([node * num_colors + c for c in range(1, num_colors + 1)])
    # we loop through all the edges
    for edge in G.edges():
        # we loop through all the colors
        for c in range(1, num_colors + 1):
            # Edges must not connect nodes of the same color
            clauses.append([-(edge[0] * num_colors + c), -(edge[1] * num_colors + c)])

    num_clauses = len(clauses)  # Number of clauses
    # # Write to DIMACS CNF file
    with open(file_name, 'w') as file:
        file.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            file.write(" ".join(map(str, clause)) + " 0\n")

def main():
    for p in PROBABILITY_VALUES:
        sub_folder = os.path.join(output_folder, f"p_{p}")
        if not os.path.exists(sub_folder):
            os.makedirs(sub_folder)
        counter = 0  # initialise the counter
        while counter < NUM_OF_INSTANCES_PER_PROBABILITY + 1:
            G_ring_lattice = generate_ring_lattice(num_vertices=NUM_VERTICES, num_neighbors=NUM_OF_NEIGHBOURS_PER_NODE)
            G_random = generate_random_graph(num_vertices=NUM_VERTICES, num_edges=NUM_EDGES)
            G_morph = morph_graphs(G_ring_lattice, G_random, p)
            # Filter out instances with chromatic number != NUM_OF_COLORS
            chromatic_number = nx.algorithms.coloring.greedy_color(G_morph)
            if len(set(chromatic_number.values())) == NUM_OF_COLORS:
                file_name = f"instance_{p}_{counter + 1}.cnf"
                graph_to_dimacs_cnf(G=G_morph, file_name=os.path.join(sub_folder, file_name), num_colors=NUM_OF_COLORS)
                print(f"Instance {file_name} created with p={p}.")
                counter += 1

# lets specify the folder to save the results to
cwd = os.getcwd()
output_folder = os.path.join(cwd, 'sat_encoded_morphed_gcp')
# make the directory if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# define the parameters
NUM_EDGES = 400  # Number of edges in the random graph
NUM_VERTICES = 100  # Number of vertices in the random graph
NUM_OF_NEIGHBOURS_PER_NODE = 8  # Number of neighbors to connect to in the ring lattice

PROBABILITY_VALUES = [0.01, 0.1, 0.2, 0.3]  # Morphing ratios
NUM_OF_INSTANCES_PER_PROBABILITY = 10  # Number of instances per morphing ratio
NUM_OF_COLORS = 5  # Number of colors to use in the graph coloring problem

main()