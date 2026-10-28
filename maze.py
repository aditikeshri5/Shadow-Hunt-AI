
import random
from collections import deque

import pygame

# Maze settings
TILE_SIZE = 32
COLS = 21
ROWS = 15

# Cyberpunk neon colour palette
BACKGROUND = (5, 8, 20)
FLOOR_COLOR = (9, 15, 31)
WALL_COLOR = (0, 38, 52)
NEON_CYAN = (0, 230, 255)

# Shared colours used by game.py
CYAN = NEON_CYAN
WHITE = (230, 245, 255)
RED = (255, 45, 85)
GREEN = (55, 255, 160)
GOLD = (255, 205, 55)


class Maze:
    def __init__(self, randomize=False):
        self.grid = self.create_maze(randomize)

    def create_maze(self, randomize=False):
        grid = [["." for _ in range(COLS)] for _ in range(ROWS)]

        # Outer boundary
        for x in range(COLS):
            grid[0][x] = "#"
            grid[ROWS - 1][x] = "#"

        for y in range(ROWS):
            grid[y][0] = "#"
            grid[y][COLS - 1] = "#"

        def horizontal_wall(y, x1, x2, gaps=()):
            for x in range(x1, x2 + 1):
                if x not in gaps:
                    grid[y][x] = "#"

        def vertical_wall(x, y1, y2, gaps=()):
            for y in range(y1, y2 + 1):
                if y not in gaps:
                    grid[y][x] = "#"

        # Original maze layout
        vertical_wall(5, 1, 5, gaps=(3,))
        vertical_wall(10, 2, 7, gaps=(5,))
        vertical_wall(15, 1, 5, gaps=(2,))

        horizontal_wall(4, 2, 8, gaps=(4,))
        horizontal_wall(8, 3, 12, gaps=(7,))
        horizontal_wall(10, 10, 18, gaps=(14,))

        vertical_wall(7, 6, 12, gaps=(9,))
        vertical_wall(13, 5, 10, gaps=(7,))

        if randomize:
            # Add random walls only when every open cell remains reachable.
            # This prevents crystals or the exit becoming trapped.
            added_walls = 0

            for _ in range(250):
                if added_walls >= 12:
                    break

                x = random.randint(2, COLS - 3)
                y = random.randint(2, ROWS - 3)

                if grid[y][x] == "#":
                    continue

                grid[y][x] = "#"

                if self.all_floor_cells_connected(grid):
                    added_walls += 1
                else:
                    grid[y][x] = "."

        return grid

    @staticmethod
    def all_floor_cells_connected(grid):
        floors = {
            (x, y)
            for y in range(ROWS)
            for x in range(COLS)
            if grid[y][x] != "#"
        }

        if not floors:
            return False

        start = next(iter(floors))
        visited = {start}
        queue = deque([start])

        while queue:
            x, y = queue.popleft()

            for nx, ny in (
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ):
                if (
                    0 <= nx < COLS
                    and 0 <= ny < ROWS
                    and grid[ny][nx] != "#"
                    and (nx, ny) not in visited
                ):
                    visited.add((nx, ny))
                    queue.append((nx, ny))

        return visited == floors

    def is_walkable(self, position):
        x, y = position
        return (
            0 <= x < COLS
            and 0 <= y < ROWS
            and self.grid[y][x] != "#"
        )

    def get_neighbors(self, position):
        x, y = position
        neighbors = []

        for dx, dy in (
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ):
            next_position = (x + dx, y + dy)

            if self.is_walkable(next_position):
                neighbors.append(next_position)

        return neighbors

    def draw(self, screen):
        for y in range(ROWS):
            for x in range(COLS):
                rect = pygame.Rect(
                    x * TILE_SIZE,
                    y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE,
                )

                if self.grid[y][x] == "#":
                    pygame.draw.rect(screen, WALL_COLOR, rect)
                    pygame.draw.rect(
                        screen,
                        NEON_CYAN,
                        rect.inflate(-5, -5),
                        1,
                    )
                else:
                    pygame.draw.rect(screen, FLOOR_COLOR, rect)
                    pygame.draw.rect(
                        screen,
                        (14, 26, 44),
                        rect,
                        1,
                    )
