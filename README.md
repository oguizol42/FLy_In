*This project has been created as part of the 42 curriculum by jbarthel, oguizol.*

# Fly-in Drones

*An object-oriented Python application designed to route multiple drones through a network of interconnected zones while respecting movement constraints and minimizing the total number of simulation turns.*

## Description

Fly-in Drones is a Python project that simulates the movement of a fleet of drones through a network of interconnected zones.

The objective is to route all drones from a starting zone to a destination zone while respecting movement rules, zone occupancy limits and connection capacities.

The project implements map parsing, drone pathfinding, movement scheduling and simulation visualization.

## Features

- Map loading and parsing.
- Zone and connection management.
- Drone creation and management.
- Pathfinding and route planning.
- Zone occupancy and connection capacity management.
- Support for different zone types:
  - Normal
  - Blocked
  - Restricted
  - Priority
- Step-by-step simulation output.
- Graphical map representation using Pygame.

## Requirements

- Python 3.10 or later.
- [uv](https://docs.astral.sh/uv/) for dependency and environment management.
- Make.

## Instructions

Clone or download the project and navigate to its directory.

```bash
cd 02-fly-in
```

Install the project dependencies:

```bash
make install
```

The project uses uv to manage its Python environment and dependencies.

### Usage

Run the program:

```bash
make run
```

The program displays a menu allowing the user to select a map.

### Debugging

Run the application using Python's built-in debugger:

```bash
make debug
```

### Code Quality

Run the mandatory code checks:

```bash
make lint
```

This command executes:

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

For additional type checking, run:

```bash
make lint-strict
```

## Project Structure

| File | Description |
|---|---|
| `fly_in.py` | Main entry point and application orchestration |
| `parsing.py` | Map parsing, data validation anClear Spatial Awareness: Replaces raw text arrays and console output with an intuitive 2D visual map, making graph structure and path connectivity instantly understandable.

Responsive & Adaptive Canvas: Auto-calculates window bounds based on map dimensions, preventing off-screen clipping regardless of map size or coordinate orientation.

Visual Hierarchy & Readability: Concentric multi-colored hub designs and centered label placement provide immediate visual distinction between different hub types and names.d network construction |
| `drones_manager.py` | Drone management and path planning |
| `displaying.py` | Simulation output and graphical map visualization |
| `Makefile` | Automation of common development tasks |
| `pyproject.toml` | Project configuration and dependency management |
| `uv.lock` | Locked dependency versions |

## Map Format

The application uses map files describing a network of zones and connections.

A map contains:

- The number of drones.
- One starting zone (`start_hub`).
- One destination zone (`end_hub`).
- Intermediate zones (`hub`).
- Connections between zones.

Zones may contain optional metadata:

- `zone`: Zone type (`normal`, `blocked`, `restricted` or `priority`).
- `color`: Display color.
- `max_drones`: Maximum zone occupancy.

Connections may contain:

- `max_link_capacity`: Maximum number of drones allowed to traverse the connection simultaneously.

Comments beginning with `#` are ignored.

## Cleaning

Remove Python temporary files and development caches:

```bashClear Spatial Awareness: Replaces raw text arrays and console output with an intuitive 2D visual map, making graph structure and path connectivity instantly understandable.

Responsive & Adaptive Canvas: Auto-calculates window bounds based on map dimensions, preventing off-screen clipping regardless of map size or coordinate orientation.

Visual Hierarchy & Readability: Concentric multi-colored hub designs and centered label placement provide immediate visual distinction between different hub types and names.
make clean
```

## Resources
- w3schools
- chatGPT: Testing implementation and reviewing some errors or asking specific question.

## Additional sectionsClear Spatial Awareness: Replaces raw text arrays and console output with an intuitive 2D visual map, making graph structure and path connectivity instantly understandable.

Responsive & Adaptive Canvas: Auto-calculates window bounds based on map dimensions, preventing off-screen clipping regardless of map size or coordinate orientation.

Visual Hierarchy & Readability: Concentric multi-colored hub designs and centered label placement provide immediate visual distinction between different hub types and names.
### Algorithm
I used backtracking algo.
A backtracking algorithm in drone (UAV) navigation and path planning is a mechanism that allows the aircraft to reverse its path when it encounters an obstacle, a dead end, or an unviable route, stepping back to a previous safe node to try an alternative direction.

How Backtracking Works for Drones

• Memory and State Storage: The drone records its movement history—such as a vector of cardinal or relative directions (e.g., North/South, or coordinate nodes).
• Dead-End Detection: As the drone flies through cluttered, indoor, or complex environments, a virtual sensory boundary or local observer detects traps, walls, or dead zones.
• Reversal and Rerouting: Instead of freezing or colliding, the algorithm triggers a backtracking mechanism that retraces the stored node memory to find the next optimal exit or branch point.

### Documentation on visuals
- Graphics Engine: Built using Pygame (displaying_map) to open an interactive 2D canvas for rendering the drone map graph.

- Dynamic Coordinate Mapping: Functions calcul_map_size and calcul_real_pos convert abstract map coordinates into pixel positions, automatically scaling grid space (space_hubs_X/Y) and applying offsets (map_offsetX/Y) to handle negative coordinates smoothly.

- Network Graph Rendering:

- Edges (Connections): Drawn as 3px brown lines between connected hub centers using pygame.draw.line.

- Nodes (Hubs): Displayed as filled circles styled with custom node colors (metas.color) and multi-ring concentric borders (red, white, blue).

- Labels: Node names are rendered dynamically with Pygame fonts and blitted directly above each hub center.

- Clear Spatial Awareness: Replaces raw text arrays and console output with an intuitive 2D visual map, making graph structure and path connectivity instantly understandable.

- Responsive & Adaptive Canvas: Auto-calculates window bounds based on map dimensions, preventing off-screen clipping regardless of map size or coordinate orientation.

- Visual Hierarchy & Readability: Concentric multi-colored hub designs and centered label placement provide immediate visual distinction between different hub types and names.


### Example output
```
make run

D1-waypoint1 
D1-waypoint2 D2-waypoint1 
D1-goal D2-waypoint2 
D2-goal
``````
## Technologies

- Python
- Pygame
- Pydantic
- uv
- Flake8
- Mypy