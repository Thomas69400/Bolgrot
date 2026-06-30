# Bolgrot

A turn‑based, isometric grid survival game built with [pygame](https://www.pygame.org/).
You play a lone character on a diamond‑shaped map. Each turn a new wave of
**flames** spawns; the boss **Bolgrot** sits on the board as an indestructible
obstacle. Survive every wave and clear the board of flames to win — run out of
HP and you lose.

The project is also designed to be driven *headlessly* by an AI: all game rules
live in a pure‑Python `Game` class with **no pygame dependency**, so the logic
can be stepped programmatically (e.g. by a NEAT/neural‑network runner) as well
as played by a human.

---

## Gameplay

- The map is a diamond of isometric tiles loaded from a text file
  (`src/config/bolgrot.map`).
- Every **120 seconds** (one turn), a flame **wave** spawns. Exactly
  `NB_WAVES` (6) distinct waves spawn over a game — no repeats.
- The player has **40 HP** and **10 AP** (action points, refreshed each turn)
  and three spells.
- Once all `NB_WAVES` waves have spawned, the player loses **1 HP per turn** —
  pressure to finish clearing the board quickly.
- **Win:** all waves have spawned *and* no flames remain on the map.
- **Lose:** the player's HP drops to 0 (a flame moving onto the player, or a
  flame that cannot be pushed, is lethal).

### Spells

| Key | Name          | Type        | Range | AP | Uses/turn | Effect |
|-----|---------------|-------------|-------|----|-----------|--------|
| `1` | Astral leap   | Line        | 1     | 1  | unlimited | Teleport 1 tile; −1 HP; landing on a flame kills it and restores 1 HP; then all flames are attracted one tile toward you. |
| `2` | Double leap   | Line        | 2     | 2  | 2         | Same as Astral leap but range 2. |
| `3` | Inaction      | Diagonal    | 1     | 1  | unlimited | Attract all flames one tile toward a target tile (no line‑of‑sight needed); −5 HP; flames can't kill you while casting. |

**Flame attraction** is the core mechanic shared by every spell: flames are
sorted nearest‑first (Manhattan distance) and each moves **one** tile toward the
player along its axis of greatest distance, staying inside its quadrant. If the
target tile is a wall or off‑map, the flame falls back to BFS pathfinding.

### Controls

| Input            | Action |
|------------------|--------|
| `1` / `2` / `3`  | Select the spell at that slot (shows its previsualisation tiles) |
| Left click       | Cast the selected spell on a highlighted tile, click a spell icon, or hit the end‑turn button |
| `SPACE`          | End the turn immediately (spawns the next wave) |
| `ESC`            | Quit |

---

## Running the project

Dependencies are managed with [`uv`](https://github.com/astral-sh/uv) and locked
in `uv.lock`. A local `.venv` is used.

```bash
make install      # uv sync — install dependencies
make run          # install + launch the game
make clean        # remove __pycache__, build/test caches
make lint         # flake8 + mypy

# or directly:
uv run python -m src
```

Once installed, the packaged console script `bolgrot` is also available.

---

## How it's built

### Architecture overview

The codebase is split so that **all rules live in pygame‑free modules** and
pygame only appears in the rendering and event‑loop layers.

```
src/
├── __main__.py     # pygame event loop only — translates input into Game calls
├── game.py         # Game: owns all state + the turn/action API (no pygame)
├── renderer.py     # Renderer: all drawing; never mutates game state
├── actions.py      # stateless click/hover hit‑testing helpers
├── constant.py     # all magic numbers + resource paths
├── entity/         # Entity (ABC) → Player, Bolgrot, Flame
├── spells/         # Spells (ABC) → ShortJump, LongJump, MoveFlames
├── map/            # Map: dict[(x,y) → Case], parses bolgrot.map
├── case/           # Case (grid cell) + CaseType enum, iso draw + hit‑test
├── BFS/            # 4‑directional breadth‑first pathfinding
├── button/         # Button widget for the end‑turn button
├── patterns/       # Patterns: the flame spawn‑wave pool (+ patterns.json)
├── config/         # bolgrot.map — the map layout
└── sprites_png/    # spell icons (.png, with .xcf GIMP sources)
```

**Separation of concerns**
- `Game` exposes the action API (`select_spell`, `play_selected_spell`,
  `clear_previsu`, `end_turn`, `reset`) and holds no rendering code. It also
  carries stubbed `step()` / `get_observation()` hooks for a future AI runner.
- `Renderer` receives game state as arguments and only draws — it never mutates
  state.
- `__main__.py` is purely the input → `Game` glue and the draw loop.

### Map representation

`Map.cases` is a `dict[tuple[int, int], Case]` keyed by `(x, y)`, giving O(1)
lookups. The map is parsed from a symbol grid in `bolgrot.map`
(`.` = free, `#` = wall, `|` = empty, `N` = no cell). Each `Case` holds its
coordinates, an optional `entity`, and a `case_type`.

### Isometric coordinate system

Grid → screen conversion is done inline wherever needed:

```
iso_x = (x - y) * (CASE_WIDTH  / 2)
iso_y = (x + y) * (CASE_HEIGHT / 2)
```

All rendering is relative to an `offset` (the screen pixel position of iso
origin `(0, 0)`), computed once to centre the map. The inverse (mouse → grid)
lives in `Case.contains()` and `actions.on_previsu_click()`.

### Dependency layering (acyclic)

Imports form a clean DAG:

```
constant → entity → case/map → BFS → spells → game
```

`Player` is deliberately **spell‑agnostic** (it imports `Spells` only under
`TYPE_CHECKING`); `Game.__init__` constructs the concrete spells with one shared
`BFS(map)` and assigns them. Because `entity` doesn't depend on the higher
layers, every module imports cleanly regardless of entry point.

### Flame spawn patterns

`Patterns` loads a vocabulary of 3‑tile "atoms" from `patterns.json` and builds
the legal wave pool as the union of two atoms (excluding spatially‑overlapping
pairs). A seeded `random.Random` makes a run's wave sequence **reproducible**.

- `draw_opening()` picks the first wave from a fixed opening set.
- `draw(occupied)` picks each subsequent wave **without replacement**, and
  **prioritises patterns that land on unoccupied cells**: it scores every
  remaining pattern by how many of its tiles overlap occupied tiles (flames or
  the player), keeps only those with the fewest overlaps, and randomly selects
  among them. Any residual occupied tiles are then dropped from the returned
  wave, so a flame is never spawned on top of an existing flame or the player.

`Game.end_turn()` places the current wave, advances the turn, then draws the
next wave passing in `Game._occupied_tiles()` (the set of tiles currently
holding a flame or the player).

### Packaging & resources

`src` is a regular package. Data files (`config/*.map`, `sprites_png/*.png`,
`patterns/*.json`) are declared as `package-data` and resolved at runtime via
`importlib.resources.files("src") / ...`, so they work from any working
directory, not just the repo root. Sprite images are lazy‑loaded on first
access.

### Tooling

- **`uv`** for dependency management and running.
- **`mypy`** for static type checking (the codebase is fully type‑annotated;
  `from __future__ import annotations` is used throughout).
- **`flake8`** for linting.
