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

### Map representation

`Map.cases` is a `list[dict[tuple[int,int], int | Entity]]` — each element is a single-entry dict mapping a grid coordinate to either `0` (empty) or an `Entity` instance. This flat list (not a 2D array) is the canonical data structure threaded through every system.

The playable area is a trimmed diamond cut from a 37×34 rectangular grid. `Map.cut_map()` calls four directional trim methods plus `remove_extra()` to produce the irregular diamond shape. After trimming, `Map.clean_map()` shifts all coordinates so they start at (0,0) and updates `constant.GRID_MAX_X/Y`.

### Coordinate system

`grid_to_iso(x, y)` converts grid coords to isometric screen offsets:
- `iso_x = (x - y) * (CASE_WIDTH / 2)`
- `iso_y = (x + y) * (CASE_HEIGHT / 2)`

The origin is centered on screen (`screen.get_width() // 2`, `screen.get_height() // 4`). `hover_tile()` is the inverse — maps a screen mouse position back to grid coords.

### Entity hierarchy

```
Entity (ABC)
├── Player   — has pos_x/y, hp, base_PA, and a list of Spells
├── Bolgrot  — has pos_x/y
└── Flame    — placed by Map.place_flames()
```

`TypeEntity` enum (NONE/FLAME/PLAYER/BOLGROT) is used in rendering to switch draw color.

### Spell system

```
Spells (ABC)
├── ShortJump  ("Astral leap")  — LINE range 1
├── LongJump   ("Double leap")  — LINE range 2
└── MoveFlames ("Inaction")     — DIAGONAL range 1
```

Each spell defines `type_spell: list[tuple[TypeSpell, int]]` where `TypeSpell` is LINE/DIAGONAL/FULL and the int is range. `Spells.previsu()` computes the highlighted reachable tiles (returned as `list[tuple]` and stored in `previsualiation` in the main loop). `Spells.play()` is the execution hook — currently unimplemented (all `pass`) in all concrete spells. Line-of-sight is a `bool` field on `Spells` but not yet enforced in `previsu()`.

### Flame spawn patterns

`Patterns.spawn_patterns` is a list of patterns; each pattern is a list of grid coordinates. Each turn, one pattern is randomly drawn (without replacement) from the list and passed to `Map.place_flames()`.

### Main loop (`src/__main__.py`)

All rendering and input handling lives here. Key responsibilities:
- `make_case()` — draws the grid, highlights previsu tiles (blue) and next spawn pattern (purple)
- `draw_entities()` — draws entities as colored circles over grid tiles
- `draw_spells()` — renders spell icons from `src/sprites_png/`; hovering shows a popup via `show_spell_data()`
- `on_spell()` — detects click on a spell icon, triggers `previsu()` then `play()`
- Turn advance fires either on timer expiry or "End turn" button click

### Sprite assets

Sprites are stored as both `.xcf` (GIMP source) and `.png` in `src/sprites_png/`. The spell classes currently reference `.xcf` filenames in their `sprite` field — this should be `.png` for pygame to load correctly.
