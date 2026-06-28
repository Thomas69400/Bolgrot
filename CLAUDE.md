# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
make install      # install dependencies via uv sync
make run          # install + run the game (uv run python -m src)
make clean        # remove __pycache__, build artifacts

uv run python -m src   # run directly without make
```

Dependencies are managed with `uv` and locked in `uv.lock`. The project uses a `.venv` local virtual environment. There are no tests yet; `pytest` is listed as a dev dependency for future use.

## Architecture

This is a pygame turn-based isometric grid game. The player tries to survive on a diamond-shaped map while Bolgrot (the boss enemy) and flame tiles threaten them. Each turn lasts 120 seconds; at the end of a turn, a new flame spawn pattern is placed on the map.

### Module responsibilities

- `src/game.py` — `Game` class: owns all game state and exposes the action API (`select_spell`, `play_selected_spell`, `clear_previsu`, `end_turn`, `reset`). Contains stubbed `step()` and `get_observation()` methods (currently commented out) as future entry points for a NEAT/AI runner. **No pygame dependency** — can be imported and run headlessly.
- `src/renderer.py` — `Renderer` class: holds rendering state (screen offset, end-turn button, spell render list). All drawing methods receive game state as arguments and never mutate it. `_compute_map_offset()` (static method) calculates the isometric origin that centers the map on screen.
- `src/__main__.py` — pygame event loop only. Translates user input into `Game` method calls; passes game state to `Renderer` methods. Keyboard: `SPACE` ends the turn; `1`/`2`/`3` select the player's spell at index 0/1/2 (via `game.select_spell(event.key - pygame.K_1)`); `ESC` quits.
- `src/constant.py` — all magic numbers including layout constants (`RIGHT_PANEL_W`, `BUTTON_W`, `BUTTON_H`, `SPELL_GAP`) and map config path (`MAP_CONF`).
- `src/actions.py` — stateless click/hover helpers: `on_previsu_click()`, `on_spell_hover()`, `on_button_end_turn_click()`.
- `src/BFS/bfs.py` — `BFS` class: 4-directional breadth-first pathfinding over `Map.cases` (walls excluded). `find_path(start, goal)` returns the **single next step** toward the goal (one coordinate tuple) or `None`. Each `Spells` instance holds a `BFS` (assigned in `Game.__init__`); used as the fallback movement when the greedy quadrant step is blocked.
- `src/case/case.py` — `Case` class (grid cell with `x`, `y`, `entity`, `case_type`) and `CaseType` enum (`FREE`, `WALL`, `EMPTY`). `Case.draw()` handles isometric rendering and `Case.contains()` does mouse hit-testing.
- `src/button/button.py` — `Button` class for the end-turn button.

### Map representation

`Map.cases` is a `dict[tuple[int, int], Case]` keyed by `(x, y)` — lookups (`Map.place_entity`, `Spells._find_case`, `BFS.is_valid_position`) are O(1) `cases.get(pos)`. Iterate values with `for case in cases.values()`. Each `Case` holds its grid coordinates (`x`, `y`), an optional `entity: Entity | None`, and a `case_type: CaseType`.

The map is loaded from the packaged `src/config/bolgrot.map` (path in `constant.MAP_CONF`) by `Map.parse_map()`. The file uses a symbol grid: `.` = FREE, `#` = WALL, `|` = EMPTY, `N` = skip (no cell). After parsing, `self.grid_max_x` and `self.grid_max_y` store the bounds.

### Packaging & resource paths

`src` is a regular package (`src/__init__.py`). Data files (`src/config/*.map`, `src/sprites_png/*.png`) are declared as `[tool.setuptools.package-data]` and resolved at runtime via `importlib.resources.files("src") / ...` in `constant.MAP_CONF` and `constant.SPRITES_DIR` — so they work regardless of the current working directory (not just from the repo root). The game has a console-script entry point `bolgrot = "src.__main__:main"`; `__main__.py` exposes `main()` (called both by the entry point and the `if __name__ == "__main__"` guard for `python -m src`).

### Coordinate system

Iso conversion is done inline wherever needed:
- `iso_x = (x - y) * (CASE_WIDTH / 2)`
- `iso_y = (x + y) * (CASE_HEIGHT / 2)`

All rendering uses `offset: tuple[int, int]` — the screen pixel position of iso origin (0,0), stored on the `Renderer` instance. The inverse (mouse → grid) is computed in `Case.contains()` and in `on_previsu_click()` in `actions.py`.

### Entity hierarchy

```
Entity (ABC)
├── blocks_sight: bool = True   (Player overrides to False)
├── killable: bool = True        (Bolgrot overrides to False)
├── Player   — pos_x/y, hp, base_PA, pa (current AP), list[Spells]
├── Bolgrot  — pos_x/y, killable=False
└── Flame    — pos_x/y
```

### Spell system

```
Spells (ABC)
├── ShortJump  ("Astral leap")  — LINE range 1, implemented play()
├── LongJump   ("Double leap")  — LINE range 2, implemented play(), tracks time_used
└── MoveFlames ("Inaction")     — DIAGONAL range 1, line_of_sight=False, attracts all flames toward the player
```

The `Spells.__init__` signature takes a `bfs: BFS` argument (after `type_spell`, before `line_of_sight`). `Game.__init__` builds one `BFS(self.map)` and assigns it to every spell.

Each spell defines `type_spell: list[tuple[TypeSpell, int]]` where `TypeSpell` is LINE/DIAGONAL/FULL and the int is range. `Spells.previsu()` computes reachable tiles using `is_in_map()`, `is_blocked_by_sight()`, and `is_entity_killable()` — line-of-sight IS enforced in `previsu()` via the `line_of_sight` bool. All three concrete spells have implemented `play()` methods.

Spells also carry `cost` (AP cost), `max_use`, `time_used` (base-class attr, default 0), `effects: list[str]`, and render a tooltip on hover via `_draw_tooltip()`. `Spells.is_castable(player)` returns `player.pa >= cost and time_used < max_use`. `Game.select_spell()` calls it first and refuses to build a previsualisation (clearing it) for an uncastable spell, so out-of-AP / maxed-out spells can't be selected, hovered into a previsu, or cast.

**Flame attraction** (`Spells.attract_flames`, shared by all three spells' `play()`): flames are sorted nearest-first (Manhattan) and each moves **one** tile toward the player along the axis of greatest distance — `|dx|>|dy|` steps in x, `|dy|>|dx|` steps in y, equal steps diagonally. This keeps each flame inside its quadrant relative to the player. If the chosen tile is a WALL or off-map, it falls back to `BFS.find_path`. A flame landing on the player or another flame sets `player.hp = 0`; Bolgrot blocks (flame stays). `push_flames` is currently a stub (`pass`).

**Dependency layering (acyclic).** Imports form a clean DAG: `constant` → `entity` → `case`/`map` → `BFS` → `spells` → `game`. `Player` is spell-agnostic — it holds `self.spells: list[Spells]` (empty by default; the `Spells` type is a `TYPE_CHECKING`-only import) and does **not** import `spells` or `BFS`. `Game.__init__` constructs the concrete spells (`ShortJump`/`LongJump`/`MoveFlames`) with a shared `BFS(self.map)` and assigns them to `player.spells`. Because `entity` no longer depends on the higher layers, every module imports cleanly regardless of entry point; `spells` modules import entity/case classes normally at module top level.

### Flame spawn patterns

`Patterns(seed=None)` holds `_all_patterns` (class-level list of patterns); each pattern is a list of grid coordinates. `Patterns.draw()` picks one at random (without replacement) using a seeded `random.Random` instance, making runs reproducible. Each turn, the drawn pattern is passed to `Game.end_turn()` which calls `Map.place_entity()` per position. `Patterns.reset()` restores the full pool.

### Sprite assets

Sprites are stored as both `.xcf` (GIMP source) and `.png` in `src/sprites_png/`. Spell classes reference `.png` filenames in their `sprite` field. Images are lazy-loaded on first access via the `image` property.
