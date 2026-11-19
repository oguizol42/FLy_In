*This project has been created as part of the 42 curriculum by oguizol.*

# Fly-in

## Description

Fly-in is a drone routing simulator written in object-oriented Python.

A map describes a network of zones (hubs) linked by bidirectional connections. A fleet of drones starts in the `start_hub` and must reach the `end_hub` in as few simulation turns as possible, while respecting every rule of the network:

- **Zone types**: `normal` (1 turn), `restricted` (2 turns, the drone stays on the connection during transit), `priority` (1 turn, preferred by the pathfinding) and `blocked` (never entered).
- **Zone capacity** (`max_drones`, default 1): the maximum number of drones in a zone at the same turn. The start and end hubs have no limit.
- **Connection capacity** (`max_link_capacity`, default 1): the maximum number of drones crossing a connection at the same turn.
- **Simultaneous moves**: a space freed during a turn can be used by another drone during that same turn.

The program parses and validates the map, computes a turn-by-turn plan for every drone, prints the simulation in the required format and displays the network in a graphical window.

All subject benchmark maps are solved at their optimum, including the optional Challenger map (see [Results](#results)).

## Instructions

### Requirements

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/)
- make

Dependencies (installed by `make install`): `pydantic`, `pygame`.
Development tools used by `make lint`: `flake8`, `mypy`.

### Installation

```bash
make install
```

### Running

```bash
make run
```

A menu lists the subject maps (1 to 10). Type the number of the map to simulate. The program then:

1. prints the simulation in the terminal, one line per turn;
2. opens a graphical window showing the map (close it to quit).

### Other rules

| Command | Effect |
|---|---|
| `make debug` | Runs the program with Python's debugger (`pdb`). |
| `make lint` | Runs `flake8` and `mypy` with the flags required by the subject. |
| `make lint-strict` | Runs `flake8` and `mypy --strict`. |
| `make clean` | Removes `__pycache__`, `*.pyc` and tool caches. |

### Project structure

| File | Role |
|---|---|
| `fly_in.py` | Entry point: map menu, loading and orchestration. |
| `parsing.py` | Map parsing and validation, data models (`Hub`, `Connection`, `Drone`). |
| `drones_manager.py` | Pathfinding and turn scheduling. |
| `displaying.py` | Terminal output and graphical display (Pygame). |
| `maps/` | Subject maps, by difficulty. |

## Map format

```text
nb_drones: 5
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
connection: hub-roof1
connection: hub-corridorA
connection: roof1-goal
connection: corridorA-goal [max_link_capacity=2]
```

- The first line gives the number of drones (positive integer).
- `start_hub:`, `end_hub:` and `hub:` define zones: `<name> <x> <y> [metadata]`. Names cannot contain dashes or spaces, coordinates are integers.
- Zone metadata (optional, any order): `zone=<normal|blocked|restricted|priority>`, `color=<word>`, `max_drones=<positive integer>`.
- `connection: <zone1>-<zone2> [max_link_capacity=<positive integer>]` links two previously defined zones. `a-b` and `b-a` are the same connection and cannot both appear.
- Lines starting with `#` are comments.

The parser stops with an error message on any invalid line (unknown zone type, duplicate name or connection, unknown zone in a connection, non-positive capacity, missing start hub…). A valid map with no path between the start and end hubs is reported as such, instead of running forever.

## Algorithm

The scheduler combines two strategies and keeps the faster one.

### 1. Backtracking with a reservation table

Drones are planned one after the other. Each drone gets the plan that makes it arrive the earliest, given the moves already reserved by the previous drones.

**Reservation table.** Each hub stores, for every turn, the list of drones it contains (`drones_by_time`). Each connection stores the drones crossing it at every turn (`drones_in_connect`). Once a drone's plan is chosen, it is written into these tables, so the following drones see it as occupied space.

**Earliest allowed move.** To move a drone from its hub to a neighbour, `allow_time` looks for the first turn at which:

- the destination hub has room (`max_drones`);
- the connection has room (`max_link_capacity`);
- for a restricted zone, the connection is free at turn `t` and the zone is free at turn `t + 1`, since the drone must reach the zone right after its transit.

If the destination is not available, the drone waits in its current hub, and those waiting turns are reserved too.

**Backtracking search.** `find_best_path` explores the paths recursively, depth first. At each hub, it tries every neighbour that was not already visited on the current path (no cycles), reserves the move, recurses, then removes the move to try the next neighbour. Every time the end hub is reached, the plan is compared to the best one found so far and kept if it is shorter.

**Neighbour ordering.** Before the search, the neighbours of each hub are sorted: end hub first, then `priority` zones, then `normal`, then `restricted`. `blocked` zones and the start hub are never explored. This makes the search find a good path very early.

**Pruning (branch and bound).** A plan can only become longer as the recursion goes deeper, and a plan only replaces the best one if it is strictly shorter. So as soon as the current branch cannot arrive before the best plan found so far, it is abandoned without exploring its continuations. Because the neighbour ordering finds a good path early, most branches are cut almost immediately. On the Challenger map, this brought the computation time from about 40 minutes down to a few seconds, with identical results.

### 2. Single-file fallback

Planning drones one by one is not always globally optimal: a drone can take a spot that makes all the following drones lose a turn. On maps whose throughput is limited to one drone per turn (capacity-1 gates), these delays add up. On the Challenger map, the backtracking alone arrives at 67 turns, one drone every two turns.

On such maps, the best possible schedule is to send every drone along the shortest path, one turn after the previous one. Since a space freed during a turn can be reused in that same turn, a single-file column moves forward by one zone per turn, so the last drone arrives at:

```text
length of the shortest path + (number of drones - 1)
```

After the backtracking, `backtraking_algo_optimisation` computes this value from the first drone's plan, which is the shortest path because nothing is reserved when it is planned. If it is lower than the backtracking result, all reservations are reset and each drone gets the first drone's plan, delayed by one more waiting turn at the start hub than the previous drone. On the Challenger map this gives 19 + 24 = 43 turns, the subject's optimum.

Keeping both strategies makes the program adapt to the map: the backtracking spreads drones over several paths when the map allows it, and the single file takes over when the map is a bottleneck.

### Complexity and memory

- **Backtracking:** in the worst case it is exponential in the number of hubs, since it can explore every simple path, and it is repeated for each drone. In practice, the neighbour ordering and the pruning cut most branches: every subject map is solved in a few seconds at most.
- **Reservation checks:** `allow_time` scans the turns of one hub and one connection, so it is linear in the number of turns.
- **Single-file fallback:** linear in `number of drones × path length`.
- **Caching:** paths are not cached between drones, because each drone sees a different reservation table. The reservations themselves act as the shared state between drones.
- **Memory:** the reservation tables store one entry per turn for each hub and connection, and each drone keeps its own plan, so memory is about `(hubs + connections + drones) × turns`.

### Possible improvements

- **Hybrid switch:** detect the drone from which the backtracking starts losing turns, keep the plans of the previous drones and send the following ones in single file. This would also save computation time, since the backtracking would not run for every drone.
- **Several single files in parallel:** find several paths that do not interfere and give each one its own column of drones. A path of length `L` that receives `n` drones finishes at turn `L + n - 1`, so drones are distributed to balance these values, and a path that would finish after all the others even with one drone is dropped. This is the best strategy on maps with several parallel paths.
- **Polynomial search:** replace the depth-first search with a breadth-first search on `(hub, turn)` states, which finds the earliest arrival of each drone in polynomial time.

## Results

Number of turns on the subject maps:

| Map | Drones | Optimum | Result |
|---|---|---|---|
| Easy 1 — linear path | 2 | 4 | **4** |
| Easy 2 — simple fork | 4 | 4 | **4** |
| Easy 3 — basic capacity | 4 | 4 | **4** |
| Medium 1 — dead end trap | 5 | 8 | **8** |
| Medium 2 — circular loop | 6 | 10 | **10** |
| Medium 3 — priority puzzle | 5 | 6 | **6** |
| Hard 1 — maze nightmare | 8 | 13 | **13** |
| Hard 2 — capacity hell | 12 | 16 | **16** |
| Hard 3 — ultimate challenge | 15 | 26 | **26** |
| Challenger — the impossible dream | 25 | 43 | **43** |

## Example

Input, `maps/easy/01_linear_path.txt`:

```text
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

Output (choice `1` in the menu):

```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
```

Each line is a turn. `D<id>-<zone>` means the drone arrived in that zone during the turn. A drone flying toward a restricted zone appears as `D<id>-<zone1>-<zone2>`, the name of the connection it is crossing. Drones that do not move are omitted.

## Visual representation

The terminal shows the simulation in the format required by the subject. The graphical window, built with Pygame, shows the network itself:

- **Hubs** are drawn at their map coordinates as circles filled with the color given in the map (`color=...`, yellow by default), surrounded by red, white and blue rings that make them stand out from the background.
- **`color=rainbow`** is a special value that draws the hub as seven concentric rings, red to violet.
- **Connections** are drawn as brown lines between hub centers.
- **Hub names** are written above each hub.
- **Automatic sizing:** the window size is computed from the extent of the coordinates, and negative coordinates are shifted, so the whole map is always visible.

Seeing the graph makes it easy to understand the map's topology, spot the bottlenecks and the alternative paths, and follow the drone moves printed in the terminal.

## Resources

- [Python documentation](https://docs.python.org/3/)
- [Pygame documentation](https://www.pygame.org/docs/)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [uv documentation](https://docs.astral.sh/uv/)
- [mypy documentation](https://mypy.readthedocs.io/) and [flake8 documentation](https://flake8.pycqa.org/)
- [Backtracking](https://en.wikipedia.org/wiki/Backtracking) and [branch and bound](https://en.wikipedia.org/wiki/Branch_and_bound)
- W3Schools, for Python syntax references

### Use of AI

The code of this project was written by me. AI tools were used as follows:

- **ChatGPT**: answering specific Python questions and reviewing some errors during development.
- **Claude**:
  - reviewing the code against the subject after a peer evaluation, which helped locate two capacity bugs (connection capacity compared to the zone capacity, and connections toward restricted zones not being recorded);
  - building small test maps to reproduce edge cases;
  - explaining concepts (shallow and deep copies, Pygame drawing functions, pruning);
  - discussing the algorithm's limits, which led to the single-file fallback;
  - writing this README and reviewing the Makefile.

Every suggestion was checked, tested on the subject maps and rewritten by me before being kept.
