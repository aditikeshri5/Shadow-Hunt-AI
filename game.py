
import pygame
import sys

from maze import (
    Maze, TILE_SIZE, COLS, ROWS,
    BACKGROUND, CYAN, WHITE, RED, GREEN, GOLD
)
from player import Player
from enemy import Enemy

# --------------------------------------------------
# GAME SETTINGS
# --------------------------------------------------

HUD_HEIGHT = 110
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE + HUD_HEIGHT

FPS = 60

PLAYER_START = (1, 1)
HUNTER_START = (19, 13)
EXIT_POSITION = (19, 1)

CRYSTAL_STARTS = [
    (3, 1),
    (8, 2),
    (17, 5),
    (4, 11),
    (11, 12)
]

FLOOR_COLOR = (9, 15, 31)
PORTAL_DARK = (35, 15, 35)

font = None
small_font = None
large_font = None


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption(
            "Shadow Hunt AI | Intelligent Maze Escape"
        )

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        self.clock = pygame.time.Clock()

        global font, small_font, large_font

        font = pygame.font.SysFont(
            "consolas", 19, bold=True
        )
        small_font = pygame.font.SysFont(
            "consolas", 14
        )
        large_font = pygame.font.SysFont(
            "consolas", 32, bold=True
        )

        self.reset()

    # --------------------------------------------------
    # RESET GAME
    # --------------------------------------------------

    def reset(self):
        self.maze = Maze()

        self.player = Player(PLAYER_START)
        self.enemy = Enemy(HUNTER_START)

        self.crystals = set(CRYSTAL_STARTS)

        self.game_state = "playing"

    # --------------------------------------------------
    # EVENTS AND PLAYER CONTROLS
    # --------------------------------------------------

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_r:
                    self.reset()
                    continue

                if self.game_state != "playing":
                    continue

                dx, dy = 0, 0

                if event.key in (
                    pygame.K_LEFT, pygame.K_a
                ):
                    dx = -1

                elif event.key in (
                    pygame.K_RIGHT, pygame.K_d
                ):
                    dx = 1

                elif event.key in (
                    pygame.K_UP, pygame.K_w
                ):
                    dy = -1

                elif event.key in (
                    pygame.K_DOWN, pygame.K_s
                ):
                    dy = 1

                if dx != 0 or dy != 0:
                    self.player.move(
                        dx,
                        dy,
                        self.maze,
                        self.crystals,
                        EXIT_POSITION
                    )

                    self.check_game_state()

        return True

    # --------------------------------------------------
    # UPDATE GAME LOGIC
    # --------------------------------------------------

    def update(self, dt):
        if self.game_state != "playing":
            return

        # A* + Fuzzy Logic hunter update
        self.enemy.update(
            dt,
            self.maze,
            self.player.position,
            self.player.score,
            len(CRYSTAL_STARTS)
        )

        self.check_game_state()

    def check_game_state(self):
        # Hunter catches the player
        if self.enemy.position == self.player.position:
            self.game_state = "lost"
            return

        # Player reaches unlocked exit
        if (
            self.player.position == EXIT_POSITION
            and not self.crystals
        ):
            self.game_state = "won"

    # --------------------------------------------------
    # DRAW EXIT PORTAL
    # --------------------------------------------------

    def draw_exit(self):
        x, y = EXIT_POSITION

        center = (
            x * TILE_SIZE + TILE_SIZE // 2,
            y * TILE_SIZE + TILE_SIZE // 2
        )

        color = GREEN if not self.crystals else RED

        pygame.draw.circle(
            self.screen, PORTAL_DARK, center, 15
        )

        pygame.draw.circle(
            self.screen, color, center, 12, 2
        )

        pygame.draw.circle(
            self.screen, color, center, 6, 2
        )

    # --------------------------------------------------
    # DRAW HUD
    # --------------------------------------------------

    def draw_hud(self):
        hud_y = ROWS * TILE_SIZE

        # HUD background
        pygame.draw.rect(
            self.screen,
            (8, 12, 27),
            (0, hud_y, WIDTH, HUD_HEIGHT)
        )

        # Neon top border
        pygame.draw.line(
            self.screen,
            CYAN,
            (0, hud_y),
            (WIDTH, hud_y),
            2
        )

        score = self.player.score
        total = len(CRYSTAL_STARTS)

        title = font.render(
            "SHADOW HUNT AI", True, CYAN
        )

        score_text = small_font.render(
            f"CRYSTALS: {score}/{total}",
            True, GOLD
        )

        controls = small_font.render(
            "MOVE: WASD / ARROWS   R: RESTART   ESC: QUIT",
            True, WHITE
        )

        exit_message = (
            "EXIT UNLOCKED!"
            if not self.crystals
            else "COLLECT ALL CRYSTALS TO UNLOCK EXIT"
        )

        exit_color = GREEN if not self.crystals else RED

        exit_text = small_font.render(
            exit_message, True, exit_color
        )

        self.screen.blit(title, (12, hud_y + 8))
        self.screen.blit(score_text, (12, hud_y + 38))
        self.screen.blit(controls, (205, hud_y + 12))
        self.screen.blit(exit_text, (205, hud_y + 42))

        # Hunter aggression percentage
        aggression = max(
            0, min(100, self.enemy.aggression)
        )

        aggression_text = small_font.render(
            f"HUNTER AGGRESSION: {aggression:.1f}%",
            True, RED
        )

        self.screen.blit(
            aggression_text,
            (205, hud_y + 62)
        )

        # Aggression bar dimensions
        bar_x = 205
        bar_y = hud_y + 84
        bar_width = 180
        bar_height = 10

        # Bar background
        pygame.draw.rect(
            self.screen,
            (35, 20, 35),
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=5
        )

        # Current aggression fill
        fill_width = int(
            bar_width * aggression / 100
        )

        if fill_width > 0:
            pygame.draw.rect(
                self.screen,
                RED,
                (bar_x, bar_y, fill_width, bar_height),
                border_radius=5
            )

        # Small neon border around the bar
        pygame.draw.rect(
            self.screen,
            (120, 40, 65),
            (bar_x, bar_y, bar_width, bar_height),
            width=1,
            border_radius=5
        )

    # --------------------------------------------------
    # DRAW END SCREEN
    # --------------------------------------------------

    def draw_end_screen(self):
        if self.game_state == "playing":
            return

        overlay = pygame.Surface(
            (WIDTH, ROWS * TILE_SIZE)
        )

        overlay.set_alpha(215)
        overlay.fill(BACKGROUND)

        self.screen.blit(overlay, (0, 0))

        if self.game_state == "won":
            title = "YOU ESCAPED!"
            color = GREEN
            subtitle = "MISSION COMPLETE"
        else:
            title = "THE SHADOW CAUGHT YOU"
            color = RED
            subtitle = "PRESS R TO TRY AGAIN"

        title_surface = large_font.render(
            title, True, color
        )

        subtitle_surface = font.render(
            subtitle, True, WHITE
        )

        self.screen.blit(
            title_surface,
            title_surface.get_rect(
                center=(
                    WIDTH // 2,
                    ROWS * TILE_SIZE // 2 - 20
                )
            )
        )

        self.screen.blit(
            subtitle_surface,
            subtitle_surface.get_rect(
                center=(
                    WIDTH // 2,
                    ROWS * TILE_SIZE // 2 + 25
                )
            )
        )

    # --------------------------------------------------
    # RENDER EVERYTHING
    # --------------------------------------------------

    def draw(self):
        self.screen.fill(BACKGROUND)

        self.maze.draw(self.screen)
        self.draw_exit()

        # Show the route chosen by A*
        if len(self.enemy.path) > 1:
            points = [
                (
                    x * TILE_SIZE + TILE_SIZE // 2,
                    y * TILE_SIZE + TILE_SIZE // 2
                )
                for x, y in self.enemy.path
            ]

            pygame.draw.lines(
                self.screen,
                (95, 35, 130),
                False,
                points,
                3
            )

        Player.draw_crystals(
            self.screen, self.crystals
        )

        self.player.draw(self.screen)
        self.enemy.draw(self.screen)

        self.draw_hud()
        self.draw_end_screen()

        pygame.display.flip()

    # --------------------------------------------------
    # MAIN GAME LOOP
    # --------------------------------------------------

    def run(self):
        running = True

        # Allow held keys to repeat
        pygame.key.set_repeat(150, 110)

        while running:
            dt = self.clock.tick(FPS) / 1000.0

            running = self.handle_events()

            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
