# Shadow Hunt AI — Intelligent Maze Escape Game

Shadow Hunt AI is a browser-based maze escape game developed using Python, Flask, HTML, CSS, and JavaScript. The player must navigate through a maze, collect all the crystals, and reach the exit while avoiding AI-controlled hunters.

The project demonstrates Artificial Intelligence and Soft Computing concepts through maze navigation, automated hunter movement, and maze connectivity validation.

## Features

- **Interactive Maze:** Navigate through a maze using keyboard controls.
- **Crystal Collection:** Collect crystals to increase your score and complete the mission.
- **AI Hunters:** Avoid hunters that pursue the player.
- **Multiple Difficulty Levels:**
  - Easy: 3 crystals and 1 hunter
  - Medium: 5 crystals and 1 hunter
  - Hard: 7 crystals and 2 hunters
- **New Maze:** Generate a modified maze layout.
- **Restart Mission:** Restart the current game.
- **Neon-Themed UI:** Dark background with neon-inspired visual elements.
- **Browser-Based Gameplay:** Play through a web interface powered by a Flask backend.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Game logic and backend functionality |
| Flask | Web server and API endpoints |
| HTML | Game interface structure |
| CSS | Styling and responsive design |
| JavaScript | Game rendering, controls, and API communication |
| Pygame | Used by the Python maze module for supporting functionality |

## Artificial Intelligence Concepts

### 1. Breadth-First Search (BFS)

Breadth-First Search is used in the maze module to check whether all walkable cells remain connected after random walls are added. This helps validate maze connectivity.

### 2. Randomized Maze Modification

The New Maze feature modifies the predefined maze layout by attempting to add random walls while checking connectivity. It does not currently implement a complete maze-generation algorithm such as Depth-First Search maze generation.

### 3. AI-Controlled Hunters

Hunters act as automated opponents that pursue the player. The exact pathfinding or movement algorithm depends on the implementation in the enemy and pathfinding modules.

## How to Play

1. Start the application.
2. Open the game in your browser.
3. Select a difficulty level.
4. Use the **W, A, S, D** keys or the **arrow keys** to move.
5. Collect the crystals placed throughout the maze.
6. Avoid the hunters.
7. Complete the mission by reaching the exit according to the game's rules.

## Project Structure

```text
Shadow-Hunt-AI/
│
├── web_app.py
├── maze.py
├── enemy.py
├── pathfinding.py
│
├── web/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
```

*Note: The structure above is illustrative. Adjust the filenames and folders to match your actual repository.*

## Installation and Setup

### Prerequisites

- Python 3.10 or a compatible Python version
- pip
- A modern web browser

### Steps

**1. Clone the repository**

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

**2. Open the project folder**

```bash
cd Shadow-Hunt-AI
```

**3. Install dependencies**

Install the required packages based on your project imports. For example:

```bash
pip install flask pygame
```

If your project includes a `requirements.txt` file, use:

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
python web_app.py
```

**5. Open the game**

Open the local URL displayed in your terminal, usually:

```text
http://127.0.0.1:5000
```

## API Endpoints

The Flask backend provides endpoints for game state and actions.

| Endpoint | Purpose |
|---|---|
| `/` | Serves the main game page |
| `/api/state` | Retrieves the current game state |
| `/api/move` | Processes player movement |
| `/api/tick` | Updates the game and hunter state |
| `/api/reset` | Restarts the current mission |
| `/api/new-maze` | Creates a modified maze layout |

## Future Improvements

- Implement and document a dedicated pathfinding algorithm for hunters.
- Improve hunter movement and game responsiveness.
- Add more maze layouts and levels.
- Introduce power-ups and additional game mechanics.
- Add sound effects and animations.
- Improve mobile controls and accessibility.

## Learning Outcomes

This project provides practical experience with:

- Python-based game logic.
- Flask APIs and frontend-backend communication.
- Interactive web development.
- Breadth-First Search and graph connectivity.
- Automated opponent behavior.
- Integrating Artificial Intelligence concepts into a playable game.

## Conclusion

Shadow Hunt AI combines maze exploration and survival gameplay with Artificial Intelligence concepts. It provides a foundation for further experimentation with pathfinding, intelligent agents, and more advanced game mechanics.

---

**Project:** Shadow Hunt AI — Intelligent Maze Escape Game  
**Category:** Artificial Intelligence & Soft Computing Mini-Project  
**Developed using:** Python, Flask, HTML, CSS, and JavaScript