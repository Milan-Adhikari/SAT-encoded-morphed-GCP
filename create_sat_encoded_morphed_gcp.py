from global_variables import *
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
    """Create a {p}-morph of G1 and G2."""
    V = set(G1.nodes())  # set of vertices in G1
    E1 = set(G1.edges())  # set of edges in G1
    E2 = set(G2.edges())  # set of edges in G2

    E_common = E1 & E2  # edges common to both G1 and G2
    E1_exclusive = list(E1 - E2)  # edges exclusive to G1
    E2_exclusive = list(E2 - E1)  # edges exclusive to G2
    
    # sample edges for the morph
    E_from_G1 = random.sample(E1_exclusive, int(p * len(E1_exclusive)))
    E_from_G2 = random.sample(E2_exclusive, int((1 - p) * len(E2_exclusive)))
    
    # combine edges
    E_morph = list(E_common) + E_from_G1 + E_from_G2
    
    # create the new graph with these edges and vertices
    G_morph = nx.Graph()  # create an empty graph
    G_morph.add_nodes_from(V)  # add the vertices
    G_morph.add_edges_from(E_morph)  # add the edges
    
    return G_morph

def graph_to_dimacs_cnf(G: nx.Graph, file_name: str, num_colors: int):
    """Encode the graph coloring problem as a DIMACS CNF and save to a file."""
    clauses = []  # list to store the clauses
    num_vars = G.number_of_nodes() * num_colors  # each node can be colored with specified number of colors

    """for more explanation of the code below, see the readme.txt"""
    # we loop through all the nodes 
    for node in G.nodes():
        # for a single node, at least one color must be assigned
        clauses.append([node * num_colors + c for c in range(1, num_colors + 1)])
        # but, a single node cannot have two different colors
        for i in range(1, num_colors + 1):
            for j in range(i + 1, num_colors + 1):
                # node cannot have two different colors, so we add a clause with negation of the two colors
                clauses.append([-(node * num_colors + i), -(node * num_colors + j)])
        
    # we loop through all the edges
    for edge in G.edges():
        # we loop through all the colors, because each node can be colored with the specified number of colors
        for c in range(1, num_colors + 1):
            # for each edge, the two nodes must not have the same color
            clauses.append([-(edge[0] * num_colors + c), -(edge[1] * num_colors + c)])

    num_clauses = len(clauses)  # Number of clauses
    # # Write to DIMACS CNF file
    with open(file_name, 'w') as file:
        file.write(f"p cnf {num_vars} {num_clauses}\n")
        for clause in clauses:
            file.write(" ".join(map(str, clause)) + " 0\n")

def main():
    # make the output directory if it does not exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    # for each probability value, we create the instances
    for p in PROBABILITY_VALUES:
        num_of_instances_created = 0  # number of instances created
        sub_folder_name = f"p_{p}_instances_{NUM_OF_INSTANCES_PER_PROBABILITY}"  # change the sub folder name here
        sub_folder = os.path.join(OUTPUT_FOLDER, sub_folder_name)  # create the sub folder path
        # if the sub folder does not exist, create it
        if not os.path.exists(sub_folder):
            os.makedirs(sub_folder)
        # we create the instances until we reach the specified number of instances
        while num_of_instances_created < NUM_OF_INSTANCES_PER_PROBABILITY:
            # we generate the ring lattice with the specified number of vertices and neighbors
            G_ring_lattice = generate_ring_lattice(num_vertices=NUM_VERTICES, num_neighbors=NUM_OF_NEIGHBOURS_PER_NODE)
            # we generate the random graph with the specified number of vertices and edges
            G_random = generate_random_graph(num_vertices=NUM_VERTICES, num_edges=NUM_EDGES)
            # we morph the two graphs
            G_morph = morph_graphs(G_ring_lattice, G_random, p)
            # Filter out instances with chromatic number != NUM_OF_COLORS i.e  the chromatic number
            chromatic_number_of_the_current_graph = nx.algorithms.coloring.greedy_color(G_morph)
            # we filter out the instances with chromatic number not equal to the specified number of colors
            if len(set(chromatic_number_of_the_current_graph.values())) == NUM_OF_COLORS:
                file_name = f"p_{p}_{num_of_instances_created + 1}.cnf"
                # we encode the graph coloring problem as a DIMACS CNF and save to a file
                graph_to_dimacs_cnf(G=G_morph, file_name=os.path.join(sub_folder, file_name), num_colors=NUM_OF_COLORS)
                print(f"Instance {file_name} created with p={p}.")
                num_of_instances_created += 1

if __name__ == "__main__":
    main()