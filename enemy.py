
import pygame

from pathfinding import astar
from maze import TILE_SIZE
from fuzzy_controller import FuzzyController

HUNTER_RED = (255, 45, 85)
HUNTER_GLOW = (75, 10, 30)
WHITE = (230, 245, 255)


class Enemy:
    def __init__(self, start_position):
        self.position = start_position
        self.path = []

        self.fuzzy_controller = FuzzyController()
        self.aggression = 25.0

        self.move_timer = 0.0
        self.move_interval = 0.55

    def update(
        self,
        dt,
        maze,
        player_position,
        crystals_collected=0,
        total_crystals=5
    ):
        """Update fuzzy aggression and move along an A* path."""

        # Calculate Manhattan distance to the player.
        distance = (
            abs(self.position[0] - player_position[0])
            + abs(self.position[1] - player_position[1])
        )

        # Fuzzy logic decides how aggressive the hunter is.
        self.aggression = (
            self.fuzzy_controller.calculate_aggression(
                distance,
                crystals_collected,
                total_crystals
            )
        )

        # Higher aggression means a shorter movement interval.
        self.move_interval = (
            0.55 - (self.aggression / 100.0) * 0.38
        )

        self.move_timer += dt

        if self.move_timer < self.move_interval:
            return

        self.move_timer = 0.0

        # A* still decides the route.
        self.path = astar(
            maze,
            self.position,
            player_position
        )

        # Move one cell along the calculated route.
        if len(self.path) > 1:
            self.position = self.path[1]

    def draw(self, screen):
        x, y = self.position

        center = (
            x * TILE_SIZE + TILE_SIZE // 2,
            y * TILE_SIZE + TILE_SIZE // 2
        )

        pygame.draw.circle(
            screen, HUNTER_GLOW, center, 15
        )

        pygame.draw.circle(
            screen, HUNTER_RED, center, 10
        )

        pygame.draw.circle(
            screen, WHITE, center, 3
        )
