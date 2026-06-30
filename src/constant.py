from importlib.resources import files

# 37
GRID_MAX_X = 37
# 34
GRID_MAX_Y = 34

CASE_HEIGHT = 32
CASE_WIDTH = 64

# (14,15)
BASE_PLAYER_POS = (14, 15)
# (21, 10)
BASE_BOLGROT_POS = (21, 10)

# HEXA COLOR
CASE_COLOR_1 = (205, 178, 111)
CASE_COLOR_2 = (189, 185, 132)
SPAWN_COLOR_1 = (151, 13, 158)
PREVISU_COLOR = (9, 91, 158)
BACKGROUND_POPUP = (79, 79, 61)

RIGHT_PANEL_W = 400
BUTTON_W = 200
BUTTON_H = 60
SPELL_GAP = 10

# IN SECONDS
TIME_TURN = 120

# Number of flame waves that spawn over a game (exactly this many, no repeats).
NB_WAVES = 6

# Package-data paths resolved relative to the installed `src` package so they
# work regardless of the current working directory.
MAP_CONF = str(files("src") / "config" / "bolgrot.map")
SPRITES_DIR = str(files("src") / "sprites_png")
PATTERNS_CONF = str(files("src") / "patterns" / "patterns.json")
