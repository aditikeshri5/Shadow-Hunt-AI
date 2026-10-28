
import pygame

from maze import TILE_SIZE

PLAYER_BLUE = (45, 100, 255)
PLAYER_CYAN = (0, 230, 255)
PLAYER_GLOW = (0, 55, 85)

CRYSTAL_GOLD = (255, 205, 55)


class Player:
    def __init__(self, start_position):
        self.position = start_position
        self.score = 0

    def move(self, dx, dy, maze, crystals, exit_position):
        """
        Move the player one cell if the destination is valid.
        Collect crystals and unlock the exit when all are collected.
        """

        new_position = (
            self.position[0] + dx,
            self.position[1] + dy
        )

        # Don't move through walls
        if not maze.is_walkable(new_position):
            return

        # Exit remains locked while crystals remain
        if new_position == exit_position and crystals:
            return

        self.position = new_position

        # Collect a crystal
        if self.position in crystals:
            crystals.remove(self.position)
            self.score += 1

    def draw(self, screen):
        x, y = self.position

        center = (
            x * TILE_SIZE + TILE_SIZE // 2,
            y * TILE_SIZE + TILE_SIZE // 2
        )

        # Neon glow
        pygame.draw.circle(
            screen, PLAYER_GLOW, center, 15
        )

        # Player body
        pygame.draw.circle(
            screen, PLAYER_BLUE, center, 10
        )

        pygame.draw.circle(
            screen, PLAYER_CYAN, center, 6
        )

    @staticmethod
    def draw_crystals(screen, crystals):
        for x, y in crystals:
            center = (
                x * TILE_SIZE + TILE_SIZE // 2,
                y * TILE_SIZE + TILE_SIZE // 2
            )

            points = [
                (center[0], center[1] - 8),
                (center[0] + 7, center[1]),
                (center[0], center[1] + 8),
                (center[0] - 7, center[1])
            ]

            # Glow behind the crystal
            pygame.draw.circle(
                screen, (55, 45, 25), center, 12
            )

            pygame.draw.polygon(
                screen, CRYSTAL_GOLD, points
            )

            pygame.draw.polygon(
                screen, (255, 245, 180), points, 1
            )
