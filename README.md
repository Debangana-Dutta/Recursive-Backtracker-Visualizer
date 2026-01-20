# Recursive Backtracker Visualizer
Maze Generation (DFS): The project uses Depth First Search to explore the grid. When the generator reaches a cell with no unvisited neighbors, it uses a Stack to backtrack to the previous node, ensuring a "perfect maze" with no loops.

Pathfinding Logic (BFS Potential): While the generation is DFS-based, you can mention that the architecture is ready for Breadth First Search (BFS) implementation to find the shortest path between the Start and End nodes.

Wall Representation: Each cell in the 2D Matrix stores a list of four Boolean values. These act as bitmasks to determine if a wall exists at the Top, Right, Bottom, or Left boundaries of that specific coordinate.

Data Structures: The project heavily relies on Lists for grid representation and a Stack for managing the recursive state during the generation phase.


# How to Run
1. Install dependencies: `pip install pygame`
2. Execute the engine: `python 2d_maze.py`
