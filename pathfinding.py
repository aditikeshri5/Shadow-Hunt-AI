
import heapq


def heuristic(a, b):
    """
    Estimate the distance between two cells using Manhattan distance.
    a and b are (x, y) positions.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(maze, start, goal):
    """
    Find a path from start to goal using A*.

    maze: Maze object
    start: (x, y) starting position
    goal: (x, y) target position

    Returns a list of positions, including start and goal.
    Returns [] if no path exists.
    """

    if not maze.is_walkable(start) or not maze.is_walkable(goal):
        return []

    if start == goal:
        return [start]

    # Priority queue: (estimated total cost, position)
    open_set = [(heuristic(start, goal), start)]

    # Previous cell for reconstructing the path
    came_from = {}

    # Actual cost from start to each discovered cell
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = [current]

            while current in came_from:
                current = came_from[current]
                path.append(current)

            path.reverse()
            return path

        for neighbor in maze.get_neighbors(current):
            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = (
                    tentative_g + heuristic(neighbor, goal)
                )

                heapq.heappush(
                    open_set,
                    (f_score, neighbor)
                )

    return []
