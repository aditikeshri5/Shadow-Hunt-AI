
from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import random
import threading
import os

from maze import Maze, COLS, ROWS
from player import Player
from enemy import Enemy
from game import PLAYER_START, HUNTER_START, EXIT_POSITION, CRYSTAL_STARTS

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"

game_lock = threading.Lock()

DIFFICULTIES = {
    "easy": {"crystals": 3, "hunters": 1, "speed": 0.035},
    "medium": {"crystals": 5, "hunters": 1, "speed": 0.05},
    "hard": {"crystals": 7, "hunters": 2, "speed": 0.07},
}

# Safe starting positions for the two Hunters
HUNTER_STARTS = [
    HUNTER_START,
    (1, ROWS - 2),
]


class BrowserGame:
    def __init__(self):
        self.difficulty = "medium"
        self.reset(new_maze=False)

    def reset(self, new_maze=False, difficulty=None):
        if difficulty in DIFFICULTIES:
            self.difficulty = difficulty

        settings = DIFFICULTIES[self.difficulty]

        self.maze = Maze(randomize=new_maze)
        self.player = Player(PLAYER_START)
        self.enemies = [
            Enemy(HUNTER_STARTS[i])
            for i in range(settings["hunters"])
        ]

        # Select different crystal positions for each new mission.
        blocked_positions = {
            PLAYER_START,
            EXIT_POSITION,
            *HUNTER_STARTS[:settings["hunters"]],
        }

        available_positions = [
            (x, y)
            for y in range(1, ROWS - 1)
            for x in range(1, COLS - 1)
            if self.maze.is_walkable((x, y))
            and (x, y) not in blocked_positions
        ]

        selected = random.sample(
            available_positions,
            min(settings["crystals"], len(available_positions)),
        )
        self.crystals = set(selected)
        self.game_state = "playing"

    def check_game_state(self):
        if any(
            enemy.position == self.player.position
            for enemy in self.enemies
        ):
            self.game_state = "lost"
        elif (
            self.player.position == EXIT_POSITION
            and not self.crystals
        ):
            self.game_state = "won"

    def get_state(self):
        settings = DIFFICULTIES[self.difficulty]

        return {
            "maze": self.maze.grid,
            "cols": COLS,
            "rows": ROWS,
            "player": list(self.player.position),

            # Keep the original single-Hunter fields for compatibility.
            "hunter": list(self.enemies[0].position),
            "hunter_path": [
                list(p) for p in self.enemies[0].path
            ],

            # New fields for displaying multiple Hunters.
            "hunters": [
                list(enemy.position) for enemy in self.enemies
            ],
            "hunter_paths": [
                [list(p) for p in enemy.path]
                for enemy in self.enemies
            ],

            "crystals": [
                list(p) for p in sorted(self.crystals)
            ],
            "exit": list(EXIT_POSITION),
            "score": self.player.score,
            "total_crystals": settings["crystals"],
            "aggression": max(
                enemy.aggression for enemy in self.enemies
            ),
            "hunter_count": len(self.enemies),
            "difficulty": self.difficulty,
            "game_state": self.game_state,
        }


game = BrowserGame()


@app.get("/")
def home():
    return send_from_directory(WEB_DIR, "index.html")


@app.get("/<path:filename>")
def website_files(filename):
    return send_from_directory(WEB_DIR, filename)


@app.get("/api/state")
def get_state():
    with game_lock:
        return jsonify(game.get_state())


@app.post("/api/move")
def move_player():
    data = request.get_json(silent=True) or {}

    try:
        dx = int(data.get("dx", 0))
        dy = int(data.get("dy", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid movement"}), 400

    if (dx, dy) not in {
        (-1, 0), (1, 0), (0, -1), (0, 1)
    }:
        return jsonify({"error": "Invalid direction"}), 400

    with game_lock:
        if game.game_state == "playing":
            self_crystals = game.crystals

            game.player.move(
                dx,
                dy,
                game.maze,
                self_crystals,
                EXIT_POSITION,
            )
            game.check_game_state()

        return jsonify(game.get_state())


@app.post("/api/tick")
def update_hunters():
    with game_lock:
        if game.game_state == "playing":
            settings = DIFFICULTIES[game.difficulty]

            for enemy in game.enemies:
                enemy.update(
                    settings["speed"],
                    game.maze,
                    game.player.position,
                    game.player.score,
                    game.get_state()["total_crystals"],
                )

            game.check_game_state()

        return jsonify(game.get_state())


@app.post("/api/reset")
def reset_game():
    data = request.get_json(silent=True) or {}
    difficulty = data.get("difficulty")

    if difficulty is not None and difficulty not in DIFFICULTIES:
        return jsonify({"error": "Invalid difficulty"}), 400

    with game_lock:
        game.reset(new_maze=False, difficulty=difficulty)
        return jsonify(game.get_state())


@app.post("/api/new-maze")
def new_maze():
    data = request.get_json(silent=True) or {}
    difficulty = data.get("difficulty")

    if difficulty is not None and difficulty not in DIFFICULTIES:
        return jsonify({"error": "Invalid difficulty"}), 400

    with game_lock:
        game.reset(new_maze=True, difficulty=difficulty)
        return jsonify(game.get_state())


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False,
        use_reloader=False,
    )
