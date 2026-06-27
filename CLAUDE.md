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
- `src/__main__.py` — pygame event loop only. Translates user input into `Game` method calls; passes game state to `Renderer` methods.
- `src/constant.py` — all magic numbers including layout constants (`RIGHT_PANEL_W`, `BUTTON_W`, `BUTTON_H`, `SPELL_GAP`) and map config path (`MAP_CONF`).
- `src/actions.py` — stateless click/hover helpers: `on_previsu_click()`, `on_spell_hover()`, `on_button_end_turn_click()`.
- `src/case/case.py` — `Case` class (grid cell with `x`, `y`, `entity`, `case_type`) and `CaseType` enum (`FREE`, `WALL`, `EMPTY`). `Case.draw()` handles isometric rendering and `Case.contains()` does mouse hit-testing.
- `src/button/button.py` — `Button` class for the end-turn button.

### Map representation

`Map.cases` is a `list[Case]`. Each `Case` holds its grid coordinates (`x`, `y`), an optional `entity: Entity | None`, and a `case_type: CaseType`.

The map is loaded from `./src/config/bolgrot.map` (path in `constant.MAP_CONF`) by `Map.parse_map()`. The file uses a symbol grid: `.` = FREE, `#` = WALL, `|` = EMPTY, `N` = skip (no cell). After parsing, `self.grid_max_x` and `self.grid_max_y` store the bounds.

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
└── MoveFlames ("Inaction")     — DIAGONAL range 1, line_of_sight=False, moves all flames toward target
```

Each spell defines `type_spell: list[tuple[TypeSpell, int]]` where `TypeSpell` is LINE/DIAGONAL/FULL and the int is range. `Spells.previsu()` computes reachable tiles using `is_in_map()`, `is_blocked_by_sight()`, and `is_entity_killable()` — line-of-sight IS enforced in `previsu()` via the `line_of_sight` bool. All three concrete spells have implemented `play()` methods.

Spells also carry `cost` (AP cost), `max_use`, `effects: list[str]`, and render a tooltip on hover via `_draw_tooltip()`.

### Flame spawn patterns

`Patterns(seed=None)` holds `_all_patterns` (class-level list of patterns); each pattern is a list of grid coordinates. `Patterns.draw()` picks one at random (without replacement) using a seeded `random.Random` instance, making runs reproducible. Each turn, the drawn pattern is passed to `Game.end_turn()` which calls `Map.place_entity()` per position. `Patterns.reset()` restores the full pool.

### Sprite assets

Sprites are stored as both `.xcf` (GIMP source) and `.png` in `src/sprites_png/`. Spell classes reference `.png` filenames in their `sprite` field. Images are lazy-loaded on first access via the `image` property.
