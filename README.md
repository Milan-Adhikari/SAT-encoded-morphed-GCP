**Date:** Apr 29, 2024  
**Author:** Milan Adhikari  

**Objective:**  
> The provided code aims to reproduce the gcp outlined at: [SW-GCP Benchmark](https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/SW-GCP/descr.html). 

**Instructions to Run the Code:**  
> 1. Clone the repository.  
> 2. Execute the command `pip install -r requirements.txt`.  
> 3. Define the values of the parameters in `global_variables.py`.  
> 4. Run the `create_sat_encoded_morphed_gcp.py`.  
> 5. Utilize `graphs_visualization.ipynb` for graph visualization.

## Code Structure
> `create_sat_encoded_morphed_gcp.py`: Main script for SAT encoding of morphed graph coloring.  
> `global_variables.py`: File to define parameters and global variables.  
> `graphs_visualization.ipynb`: Jupyter notebook for visualizing graphs.  

## Contributions
> Contributions to improve the code, add features, or fix bugs are welcome. Please feel free to submit a pull request.

## Explanation of code segments:
> The code includes inline comments explaining each part of the implementation, including the SAT encoding process and the logic behind each clause introduced.

### Approach Overview:  
Each node (0, 1, 2, 3, ...) can be colored in one of 5 (1, 2, 3, 4, 5) different colors.

for node 0:
    if node 0 is colored in color 1, its value is 0 * (chromatic_num = 5) + 1 = 1
    if node 0 is colored in color 2, its value is 0 * (chromatic_num = 5) + 2 = 2
    if node 0 is colored in color 3, its value is 0 * (chromatic_num = 5) + 3 = 3
    if node 0 is colored in color 4, its value is 0 * (chromatic_num = 5) + 4 = 4
    if node 0 is colored in color 5, its value is 0 * (chromatic_num = 5) + 5 = 5

for node 1:
    if node 1 is colored in color 1, its value is 1 * (chromatic_num = 5) + 1 = 6
    if node 1 is colored in color 2, its value is 2 * (chromatic_num = 5) + 2 = 7
    if node 1 is colored in color 3, its value is 3 * (chromatic_num = 5) + 3 = 8
    if node 1 is colored in color 4, its value is 4 * (chromatic_num = 5) + 4 = 9
    if node 1 is colored in color 5, its value is 5 * (chromatic_num = 5) + 5 = 10

...

So, we can see that each of the node occupies 5 values, based on the color that it is colored in.

### (line 48: create_sat_encoded_morphed_gcp.py)
> clauses.append([node * num_colors + c for c in range(1, num_colors + 1)])
> 
>     => In the above code, our intention is to introduce clause that will assign atleast 1 color to the node 
>     for each node, the code assigns a single clause that looks like this [1 ,2 ,3 ,4 ,5] (for node 0).
>     This clause states that atleast, one of the values must be true.


### (line 50: create_sat_encoded_morphed_gcp.py)
> for i in range(1, num_colors + 1):
>     for j in range(i + 1, num_colors + 1):
>         # node cannot have two different colors, so we add a clause with negation of the two colors
>         clauses.append([-(node * num_colors + i), -(node * num_colors + j)])
> 
>     => In the above code, our intention is to introduce clauses that prevent a single node from having multiple colors
>     The clauses look like this:
>         -1 -2 
>         -1 -3 
>         -1 -4 
>         -1 -5 
>         -2 -3 
>         -2 -4 
>         -2 -5 
>         -3 -4 
>         -3 -5 
>         -4 -5
>     The clauses above ensure that, the node can take only 1 color or none at all.

> So, the 2 code pieces combined together give us the guarantee that exactly 1 color is assigned to each node.

### (line 56: create_sat_encoded_morphed_gcp.py)
> for edge in G.edges():
>         # we loop through all the colors, because each node can be colored with the specified number of colors
>         for c in range(1, num_colors + 1):
>             # for each edge, the two nodes must not have the same color
>             clauses.append([-(edge[0] * num_colors + c), -(edge[1] * num_colors + c)])
> 
>     => the above code ensures that 2 connected nodes (an edge) do not have the same color.
>     the code creates clauses like, (for connecting node 0 and 1)
>     -1, -6
>     -2, -7
>     -3, -8
>     -4, -9
>     -5, -10
> 
>     We, know that if both node 0, and 1 was colored in 
>         color 1, their respective values would be 1, 6
>         color 2, their respective values would be 2, 7
>         color 3, their respective values would be 3, 8
>         color 4, their respective values would be 4, 9
>         color 5, their respective values would be 5, 10
> 
>     So, if we negate these clauses, stating atleast 1 must be false, then we can ensure that 2 connected nodes do not have the same color.
