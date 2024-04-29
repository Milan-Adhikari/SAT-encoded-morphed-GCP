"""
This file contains all the global variables that are used in the project.
"""
import os

NUM_VERTICES = 100  # define the number of vertices in the graph
NUM_EDGES = 400  # define the number of edges in the graph
# in the ring lattice, each node is connected to the below specified number of neighbors
NUM_OF_NEIGHBOURS_PER_NODE = 8  # define the number of neighbors that each node should connect to in the ring lattice
# for the specific problems, a regular ring lattice with k=8 is used, and is morphed with a random graph, but, when p=0, the chromatic number is 5
NUM_OF_COLORS = 5  # define the number of colors to use in the graph coloring problem i.e the chromatic number

# define the probability values to use in the morphing process
PROBABILITY_VALUES = [0.01, 0.2]  # Morphing ratios
# define the number of instances to create for each probability value
NUM_OF_INSTANCES_PER_PROBABILITY = 1000  # Number of instances per morphing ratio

# specify the folder name to save the results to
FOLDER_NAME = 'sat_encoded_morphed_gcp'
# lets specify the output folder to save the results to
cwd = os.getcwd()
OUTPUT_FOLDER = os.path.join(cwd, FOLDER_NAME)
