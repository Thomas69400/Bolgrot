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

- `src/game.py` — `Game` class: owns all game state and exposes the action API (`select_spell`, `end_turn`, `reset`). Contains stubbed `step()` and `get_observation()` methods (currently commented out) as future entry points for a NEAT/AI runner. **No pygame dependency** — can be imported and run headlessly.
- `src/renderer.py` — all pygame drawing functions. Receives game state as arguments; never mutates it. `compute_map_offset()` calculates the isometric origin that centers the map on screen. The right panel width and button dimensions live in `constant.py`, not here.
- `src/__main__.py` — pygame event loop only. Translates user input into `Game` method calls; passes game state to renderer functions.
- `src/constant.py` — all magic numbers including layout constants (`RIGHT_PANEL_W`, `BUTTON_W`, `BUTTON_H`, `SPELL_GAP`).

### Map representation

`Map.cases` is a `dict[tuple[int,int], int | Entity]` mapping each grid coordinate to either `0` (empty) or an `Entity` instance.

The playable area is a trimmed diamond cut from a 37×34 rectangular grid. `Map.cut_map()` calls four directional trim methods plus `remove_extra()`. After trimming, `Map.clean_map()` shifts all coordinates to start at (0,0) and stores the final bounds as `self.grid_max_x / self.grid_max_y` on the `Map` instance (does not mutate `constant.py`).

### Coordinate system

`grid_to_iso(x, y)` in `renderer.py` converts grid coords to isometric pixel offsets:
- `iso_x = (x - y) * (CASE_WIDTH / 2)`
- `iso_y = (x + y) * (CASE_HEIGHT / 2)`

All rendering functions take an `offset: tuple[int, int]` — the screen pixel position of iso origin (0,0). `hover_tile()` is the inverse, converting mouse position back to grid coords using the same offset.

### Entity hierarchy

```
Entity (ABC)
├── Player   — has pos_x/y, hp, base_PA, and a list of Spells
├── Bolgrot  — has pos_x/y
└── Flame    — placed by Map.place_flames()
```

### Spell system

```
Spells (ABC)
├── ShortJump  ("Astral leap")  — LINE range 1
├── LongJump   ("Double leap")  — LINE range 2
└── MoveFlames ("Inaction")     — DIAGONAL range 1
```

Each spell defines `type_spell: list[tuple[TypeSpell, int]]` where `TypeSpell` is LINE/DIAGONAL/FULL and the int is range. `Spells.previsu()` computes reachable tiles. `Spells.play()` is unimplemented (`pass`) in all concrete spells. Line-of-sight is a `bool` field on `Spells` but not yet enforced in `previsu()`.

### Flame spawn patterns

`Patterns(seed=None)` holds a list of patterns; each pattern is a list of grid coordinates. `Patterns.draw()` picks one at random (without replacement) using a seeded `random.Random` instance, making runs reproducible. Each turn, the drawn pattern is passed to `Map.place_flames()`.

### Sprite assets

Sprites are stored as both `.xcf` (GIMP source) and `.png` in `src/sprites_png/`. Spell classes reference `.png` filenames in their `sprite` field.
