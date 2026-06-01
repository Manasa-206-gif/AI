WIDTH, HEIGHT = 680, 680
BOARD_SIZE = 640
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_SIZE // COLS
OFFSET_X = (WIDTH - BOARD_SIZE) // 2
OFFSET_Y = (HEIGHT - BOARD_SIZE) // 2

# Default Board Colors (overridden by theme)
LIGHT_SQ   = (240, 217, 181)
DARK_SQ    = (181, 136,  99)
HIGHLIGHT  = (186, 202,  68)
MOVE_DOT   = (100, 111,  64)
CAPTURE_SQ = (220,  80,  60)

# UI Colors
BG_COLOR      = (30,  30,  35)
PANEL_COLOR   = (45,  45,  52)
TEXT_WHITE    = (240, 240, 240)
TEXT_GOLD     = (255, 215,   0)
TEXT_GRAY     = (160, 160, 170)
ACCENT_GREEN  = ( 80, 200, 120)
ACCENT_BLUE   = ( 80, 140, 220)
BUTTON_COLOR  = ( 60,  60,  70)
BUTTON_HOVER  = ( 80,  80,  95)

# Modes
MODE_MENU    = "menu"
MODE_COLOR   = "color"    # Board colour picker screen
MODE_HVH     = "hvh"
MODE_HVA     = "hva"
MODE_WINNER  = "winner"   # Winner celebration screen

# Board Themes: (name, light_sq, dark_sq)
BOARD_THEMES = [
    ("Classic",    (240, 217, 181), (181, 136,  99)),
    ("Forest",     (210, 230, 190), ( 80, 130,  70)),
    ("Ocean",      (200, 225, 245), ( 50, 100, 160)),
    ("Midnight",   (180, 180, 210), ( 50,  50,  90)),
    ("Rose",       (245, 210, 215), (180,  80,  90)),
    ("Slate",      (200, 200, 200), ( 90,  90,  90)),
    ("Gold",       (255, 240, 180), (180, 130,  20)),
    ("Candy",      (255, 200, 220), (200,  80, 140)),
]