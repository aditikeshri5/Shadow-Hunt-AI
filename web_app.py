
from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import threading

from maze import Maze, COLS, ROWS
from player import Player
from enemy import Enemy
from game import PLAYER_START, HUNTER_START, EXIT_POSITION, CRYSTAL_STARTS

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"

# This starter version supports one local game session.
game_lock = threading.Lock()


class BrowserGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.maze = Maze()
        self.player = Player(PLAYER_START)
        self.enemy = Enemy(HUNTER_START)
        self.crystals = set(CRYSTAL_STARTS)
        self.game_state = "playing"

    def check_game_state(self):
        if self.enemy.position == self.player.position:
            self.game_state = "lost"
        elif (
            self.player.position == EXIT_POSITION
            and not self.crystals
        ):
            self.game_state = "won"

    def get_state(self):
        return {
            "maze": self.maze.grid,
            "cols": COLS,
            "rows": ROWS,
            "player": list(self.player.position),
            "hunter": list(self.enemy.position),
            "hunter_path": [list(p) for p in self.enemy.path],
            "crystals": [list(p) for p in sorted(self.crystals)],
            "exit": list(EXIT_POSITION),
            "score": self.player.score,
            "total_crystals": len(CRYSTAL_STARTS),
            "aggression": self.enemy.aggression,
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
            game.player.move(
                dx,
                dy,
                game.maze,
                game.crystals,
                EXIT_POSITION,
            )
            game.check_game_state()

        return jsonify(game.get_state())


@app.post("/api/tick")
def update_hunter():
    with game_lock:
        if game.game_state == "playing":
            # Advance the existing Enemy and fuzzy/A* logic.
            game.enemy.update(
                0.05,
                game.maze,
                game.player.position,
                game.player.score,
                len(CRYSTAL_STARTS),
            )
            game.check_game_state()

        return jsonify(game.get_state())


@app.post("/api/reset")
def reset_game():
    with game_lock:
        game.reset()
        return jsonify(game.get_state())


if __name__ == "__main__":
    import os


    app.run( host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False,
        use_reloader=False,)
