
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
    def __init__(self):
        self.grid = self.create_maze()

    def create_maze(self):
        # "." means an empty cell; "#" means a wall.
        grid = [
            ["." for _ in range(COLS)]
            for _ in range(ROWS)
        ]

        # Outer boundary
        for x in range(COLS):
            grid[0][x] = "#"
            grid[ROWS - 1][x] = "#"

        for y in range(ROWS):
            grid[y][0] = "#"
            grid[y][COLS - 1] = "#"

        # Internal walls and openings
        def horizontal_wall(y, x1, x2, gaps=()):
            for x in range(x1, x2 + 1):
                if x not in gaps:
                    grid[y][x] = "#"

        def vertical_wall(x, y1, y2, gaps=()):
            for y in range(y1, y2 + 1):
                if y not in gaps:
                    grid[y][x] = "#"

        vertical_wall(5, 1, 5, gaps=(3,))
        vertical_wall(10, 2, 7, gaps=(5,))
        vertical_wall(15, 1, 5, gaps=(2,))

        horizontal_wall(4, 2, 8, gaps=(4,))
        horizontal_wall(8, 3, 12, gaps=(7,))
        horizontal_wall(10, 10, 18, gaps=(14,))

        vertical_wall(7, 6, 12, gaps=(9,))
        vertical_wall(13, 5, 10, gaps=(7,))

        return grid

    def is_walkable(self, position):
        x, y = position

        return (
            0 <= x < COLS
            and 0 <= y < ROWS
            and self.grid[y][x] != "#"
        )

    def get_neighbors(self, position):
        x, y = position

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        neighbors = []

        for dx, dy in directions:
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
                    TILE_SIZE
                )

                if self.grid[y][x] == "#":
                    pygame.draw.rect(
                        screen, WALL_COLOR, rect
                    )

                    pygame.draw.rect(
                        screen, NEON_CYAN,
                        rect.inflate(-5, -5), 1
                    )
                else:
                    pygame.draw.rect(
                        screen, FLOOR_COLOR, rect
                    )

                    pygame.draw.rect(
                        screen, (14, 26, 44), rect, 1
                    )
