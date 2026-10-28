
from maze import Maze
from pathfinding import astar

maze = Maze()

start = (1, 1)
goal = (19, 13)

path = astar(maze, start, goal)

print("Start:", start)
print("Goal:", goal)
print("Path found:", bool(path))
print("Number of cells in path:", len(path))
print("First few cells:", path[:10])

if path:
    print("Final cell:", path[-1])
