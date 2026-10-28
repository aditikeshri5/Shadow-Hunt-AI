
const mazeElement = document.getElementById("maze");
const connectionElement = document.getElementById("connection");
const scoreElement = document.getElementById("score");
const aggressionElement = document.getElementById("aggression");
const statusElement = document.getElementById("status");
const restartButton = document.getElementById("restart");
const newMazeButton = document.getElementById("newMaze");
const difficultyLabel = document.getElementById("difficultyLabel");
const hunterCountElement = document.getElementById("hunterCount");
const difficultyButtons = document.querySelectorAll(".difficulty-btn");

let gameState = null;
let busy = false;

async function apiRequest(url, method = "GET", data = null) {
    const options = { method };

    if (data !== null) {
        options.headers = { "Content-Type": "application/json" };
        options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
    }

    return response.json();
}

function samePosition(a, b) {
    return a[0] === b[0] && a[1] === b[1];
}

function drawMaze(state) {
    mazeElement.innerHTML = "";
    mazeElement.style.gridTemplateColumns =
        `repeat(${state.cols}, minmax(0, 1fr))`;

    const paths = state.hunter_paths || [state.hunter_path || []];
    const hunters = state.hunters || [state.hunter];

    const pathPositions = new Set();
    paths.forEach(path => {
        path.forEach(p => pathPositions.add(`${p[0]},${p[1]}`));
    });

    const hunterPositions = new Set(
        hunters.map(p => `${p[0]},${p[1]}`)
    );

    const crystalPositions = new Set(
        state.crystals.map(p => `${p[0]},${p[1]}`)
    );

    for (let row = 0; row < state.rows; row++) {
        for (let col = 0; col < state.cols; col++) {
            const cell = document.createElement("div");
            const key = `${col},${row}`;

            cell.className = state.maze[row][col] === "#"
                ? "cell wall"
                : "cell floor";

            if (pathPositions.has(key)) {
                cell.classList.add("path");
            }

            if (samePosition(state.exit, [col, row])) {
                cell.textContent = "✦";
                cell.classList.add("exit");
                cell.title = "Exit portal";
            }

            if (crystalPositions.has(key)) {
                cell.textContent = "◆";
                cell.classList.add("crystal");
                cell.title = "Crystal";
            }

            if (hunterPositions.has(key)) {
                cell.textContent = "☠";
                cell.classList.add("hunter");
                cell.title = "Hunter";
            }

            if (samePosition(state.player, [col, row])) {
                cell.textContent = "●";
                cell.classList.add("player");
                cell.title = "You";
            }

            mazeElement.appendChild(cell);
        }
    }

    scoreElement.textContent =
        `${state.score}/${state.total_crystals}`;

    aggressionElement.textContent =
        `${Math.round(state.aggression)}%`;

    const level = state.difficulty || "medium";
    difficultyLabel.textContent = level.toUpperCase();
    hunterCountElement.textContent =
        state.hunter_count || hunters.length;

    difficultyButtons.forEach(button => {
        button.classList.toggle(
            "active",
            button.dataset.level === level
        );
    });

    if (state.game_state === "won") {
        statusElement.textContent =
            "MISSION COMPLETE! You escaped!";
    } else if (state.game_state === "lost") {
        statusElement.textContent =
            "GAME OVER! A Hunter caught you!";
    } else if (state.score < state.total_crystals) {
        statusElement.textContent =
            `Collect all ${state.total_crystals} crystals to unlock the exit.`;
    } else {
        statusElement.textContent =
            "All crystals collected! Reach the exit!";
    }
}

async function refreshState() {
    try {
        gameState = await apiRequest("/api/state");
        connectionElement.textContent = "SYSTEM ONLINE";
        connectionElement.style.color = "#37ffa0";
        drawMaze(gameState);
    } catch (error) {
        connectionElement.textContent = "CONNECTION ERROR";
        connectionElement.style.color = "#ff2d55";
        statusElement.textContent =
            "Cannot connect to Flask. Check web_app.py.";
        console.error(error);
    }
}

async function movePlayer(dx, dy) {
    if (busy || !gameState || gameState.game_state !== "playing") {
        return;
    }

    busy = true;

    try {
        gameState = await apiRequest(
            "/api/move",
            "POST",
            { dx, dy }
        );
        drawMaze(gameState);
    } catch (error) {
        console.error("Movement failed:", error);
    } finally {
        busy = false;
    }
}

async function updateHunter() {
    if (busy || !gameState || gameState.game_state !== "playing") {
        return;
    }

    busy = true;

    try {
        gameState = await apiRequest("/api/tick", "POST");
        drawMaze(gameState);
    } catch (error) {
        console.error("Hunter update failed:", error);
    } finally {
        busy = false;
    }
}

async function restartGame() {
    if (busy) return;

    busy = true;

    try {
        gameState = await apiRequest(
            "/api/reset",
            "POST",
            { difficulty: gameState?.difficulty || "medium" }
        );
        drawMaze(gameState);
    } catch (error) {
        console.error("Restart failed:", error);
    } finally {
        busy = false;
    }
}

async function generateNewMaze() {
    if (busy) return;

    busy = true;

    try {
        gameState = await apiRequest(
            "/api/new-maze",
            "POST",
            { difficulty: gameState?.difficulty || "medium" }
        );
        drawMaze(gameState);
    } catch (error) {
        console.error("New maze failed:", error);
        statusElement.textContent =
            "Could not generate a new maze. Please try again.";
    } finally {
        busy = false;
    }
}

async function changeDifficulty(level) {
    if (busy) return;

    busy = true;

    try {
        gameState = await apiRequest(
            "/api/reset",
            "POST",
            { difficulty: level }
        );
        drawMaze(gameState);
    } catch (error) {
        console.error("Difficulty change failed:", error);
    } finally {
        busy = false;
    }
}

document.addEventListener("keydown", event => {
    const key = event.key.toLowerCase();

    const directions = {
        arrowup: [0, -1],
        w: [0, -1],
        arrowdown: [0, 1],
        s: [0, 1],
        arrowleft: [-1, 0],
        a: [-1, 0],
        arrowright: [1, 0],
        d: [1, 0]
    };

    if (["arrowup", "arrowdown", "arrowleft", "arrowright", " "].includes(key)) {
        event.preventDefault();
    }

    if (key === "r") {
        restartGame();
        return;
    }

    if (directions[key]) {
        movePlayer(...directions[key]);
    }
});

restartButton.addEventListener("click", restartGame);
newMazeButton.addEventListener("click", generateNewMaze);

difficultyButtons.forEach(button => {
    button.addEventListener("click", () => {
        changeDifficulty(button.dataset.level);
    });
});

refreshState();
setInterval(updateHunter, 250);
