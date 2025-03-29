# Constants
GRID_SIZE = 20
TILE_SIZE = 40
TOOLBAR_WIDTH = 100
WIDTH = GRID_SIZE * TILE_SIZE + TOOLBAR_WIDTH
HEIGHT = GRID_SIZE * TILE_SIZE
FPS = 60
WATER_UPDATE_DELAY = 15
WALL_THICKNESS = 3  # base thickness in setup mode

# Fallback background colors (if images not available)
SETUP_BG_COLOR = (245, 222, 179)   # Parchment look
GAME_BG_COLOR = (124, 252, 0)       # Lawn green (grass)

# Colors for grid lines, text, toolbar, etc.
DARK_BROWN = (101, 67, 33)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_COLOR = (200, 200, 200)
BUTTON_ACTIVE_COLOR = (150, 150, 150)
TOOL_COLOR = (212, 198, 161)
TOOL_ACTIVE_COLOR = (191, 179, 145)
TOOLBAR_COLOR = (104, 43, 33)
# START_BUTTON_DEFAULT_COLOR = (80, 80, 80)
# START_BUTTON_PRESSED_COLOR = (150, 150, 150)
ERASER_COLOR = (255, 105, 180)
RIVER_COLOR = (24, 77, 114)

# Animated water: full-tile water uses a water texture (with transparency)
WATER_FRAME_DURATION = 300  # milliseconds per frame

# For water in partially filled (diagonal) cells we cycle through a list of colors.
WATER_ANIM_COLORS = [
    (0, 191, 255, 180),
    (0, 181, 245, 180),
    (0, 201, 255, 180)
]

# Tool and wall types.
TOOL_HORIZONTAL = 'horizontal'
TOOL_DIAGONAL_LEFT = 'diagonal_left'
TOOL_DIAGONAL_RIGHT = 'diagonal_right'
TOOL_ERASER = 'eraser'
TOOL_NONE = None

WALL_HORIZONTAL = 'horizontal'
WALL_DIAGONAL_LEFT = 'diagonal_left'
WALL_DIAGONAL_RIGHT = 'diagonal_right'

# Tutorial configuration
TUTORIAL_MESSAGES = [
    """Welcome!
Guide water to flood the enemy's castle.
Place walls in setup phase.
Press SPACE when ready. Press R to restart.""",
    """Mountains block water permanently.""",
    """Villages must NOT be flooded! 
Keep water away from village tiles.""",
    """Farmland MUST be flooded to grow crops. 
Protect villages from flooding while 
watering crops.""",
    """Split water sources
    using a horizontal wall."""
]

# Levels configuration (5 tutorial, 8 actual)
levels = [
    {  # Level 1 - Castle introduction
        'castle_pos': (16, 19),
        'river': [(i, 0) for i in range(9, 12)],
        'obstacles': {}
    },
    {  # Level 2 - Mountain introduction
        'castle_pos': (10, 19),
        'river': [(i, 0) for i in range(9, 12)],
        'obstacles': {
            (10, 10): 'mountain',
            (9, 12): 'mountain',
            (11, 12): 'mountain'
        }
    },
    {  # Level 3 - Village introduction
        'castle_pos': (10, 19),
        'river': [(i, 0) for i in range(9, 12)],
        'obstacles': {
            (9, 15): 'village',
            (11, 15): 'village',
            (10, 10): 'mountain'
        }
    },
    {  # Level 4 - Farmland introduction
        'castle_pos': (10, 19),
        'river': [(i, 0) for i in range(9, 12)],
        'obstacles': {
            (9, 12): 'village',
            (10, 12): 'farmland',
            (11, 12): 'village',
            (10, 8): 'mountain'
        }
    },
    {  # Level 5 - Splitting water
        'castle_pos': (10, 19),
        'river': [(i, 0) for i in range(10, 11)],
        'obstacles': {
            (9, 12): 'farmland',
            (11, 12): 'farmland',
            (10, 8): 'mountain'
        }
    },
    {  # Level 1 - Basic combination
        'castle_pos': (5, 19),
        'river': [(i, 0) for i in range(3, 7)],
        'obstacles': {
            (2, 4): 'mountain', (8, 4): 'mountain',
            (5, 8): 'mountain', (7, 12): 'village',
            (5, 16): 'farmland', (12, 18): 'farmland'
        }
    },
    {  # Level 2 - Mountains
        'castle_pos': (10, 19),
        'river': [(i, 0) for i in range(9, 12)],
        'obstacles': {
            (10, 10): 'mountain',
            (10, 11): 'village',
            (8, 3): 'mountain', (9, 3): 'mountain', (10, 3): 'mountain', (11, 3): 'mountain', (12, 3): 'mountain',
            (9, 10): 'farmland', (11, 10): 'farmland',
            (9, 11): 'farmland', (11, 11): 'farmland'
        }
    },
    {  # Level 3 - Large town
        'castle_pos': (10, 19),
        'river': [(i, 0) for i in range(8, 13)],
        'obstacles': {
            (10, 9): 'village', (10, 10): 'village', (10, 11): 'village',
            (12, 9): 'village', (12, 10): 'village', (12, 11): 'village',
            (14, 9): 'village', (14, 10): 'village', (14, 11): 'village',
            (11, 9): 'farmland', (11, 10): 'farmland', (11, 11): 'farmland',
            (13, 9): 'farmland', (13, 10): 'farmland', (13, 11): 'farmland',
            (15, 9): 'mountain', (15, 10): 'mountain', (15, 11): 'mountain',
            (9, 9): 'mountain', (9, 10): 'mountain', (9, 11): 'mountain',
        }
    },
    {  # Level 4 - Not so hard
        'castle_pos': (5, 19),
        'river': [(i, 0) for i in range(0, 6)],
        'obstacles': {
            (3, 7): 'mountain', (6, 7): 'mountain',
            (3, 14): 'village', (6, 14): 'village',
            (2, 18): 'farmland', (8, 18): 'farmland',
            (5, 10): 'mountain', (0, 12): 'mountain',
            (10, 12): 'mountain'
        }
    },
    {  # Level 5 - Tricky level
        'castle_pos': (10, 19),
        'river': [(i, 0) for i in range(9, 12)],
        'obstacles': {
            (10, 15): 'farmland',
            (8, 17): 'farmland',
            (12, 17): 'farmland',
            (10, 10): 'mountain',
            (10, 11): 'village'
        }
    },
    { # Level 6 more obstacles but not hard
        'castle_pos': (10, 19),
        'river': [(i, 0) for i in range(5, 16)],  # Wide river source
        'obstacles': {
            # Circular mountain barrier
            (8, 5): 'mountain', (9, 5): 'mountain', (10, 5): 'mountain', (11, 5): 'mountain', (12, 5): 'mountain',
            (7, 6): 'mountain', (13, 6): 'mountain',
            (6, 7): 'mountain', (14, 7): 'mountain',
            (6, 8): 'mountain', (14, 8): 'mountain',
            (7, 9): 'mountain', (13, 9): 'mountain',
            (8, 10): 'mountain', (9, 10): 'mountain', (10, 10): 'mountain', (11, 10): 'mountain', (12, 10): 'mountain',
            
            # Rotating village/farmland pattern
            (3, 3): 'village', (17, 3): 'village',
            (4, 4): 'farmland', (16, 4): 'farmland',
            (5, 5): 'village', (15, 5): 'village',
            (6, 6): 'farmland', (14, 6): 'farmland',
            (7, 7): 'village', (13, 7): 'village',
            
            # Bottom protection zone
            (2, 15): 'mountain', (3, 16): 'mountain', (4, 17): 'mountain',
            (17, 15): 'mountain', (16, 16): 'mountain', (15, 17): 'mountain',
            
            # Farmland clusters
            (2, 12): 'farmland',
            (17, 12): 'farmland',
            
            # Village checkpoints
            (9, 14): 'village', (10, 14): 'village', (11, 14): 'village'
        }
    },
    { # Level 7, circle mountains
        'castle_pos': (10, 19),
        'river': [(i, 0) for i in range(9, 12)],  # Narrow river source
        'obstacles': {
            # Alternating horizontal barriers
            (0, 3): 'mountain', (1, 3): 'mountain', (2, 3): 'mountain',
            (5, 3): 'mountain', (6, 3): 'mountain', (7, 3): 'mountain',
            (13, 3): 'mountain', (14, 3): 'mountain', (15, 3): 'mountain',
            (17, 3): 'mountain', (18, 3): 'mountain', (19, 3): 'mountain',
            
            # Diamond-shaped village complex
            (8, 6): 'village', (9, 6): 'village', (10, 6): 'village', (11, 6): 'village', (12, 6): 'village',
            (7, 7): 'village', (13, 7): 'village',
            (6, 8): 'village', (14, 8): 'village',
            (7, 9): 'village', (13, 9): 'village',
            (8, 10): 'village', (9, 10): 'village', (10, 10): 'village', (11, 10): 'village', (12, 10): 'village',
            
            # Farmland channels
            (3, 5): 'farmland', (3, 7): 'farmland', (3, 9): 'farmland', (3, 11): 'farmland',
            (16, 5): 'farmland', (16, 7): 'farmland', (16, 9): 'farmland', (16, 11): 'farmland',
            
            # Water gates
            (4, 13): 'mountain', (5, 14): 'mountain', (6, 15): 'mountain',
            (15, 13): 'mountain', (14, 14): 'mountain', (13, 15): 'mountain',
            
            # Final defense line
            (8, 17): 'farmland', (9, 17): 'mountain', (10, 17): 'farmland', (11, 17): 'mountain', (12, 17): 'farmland'
        }
    },
    { # Level 8 - Even harder than last one, last level ig
        'castle_pos': (10, 19),
        'river': [(i, 0) for i in range(8, 13)],  # Central river source
        'obstacles': {
            # Vertical mountain barrier
            (10, 2): 'mountain', (10, 3): 'mountain', (10, 4): 'mountain',
            (10, 5): 'mountain', (10, 6): 'mountain', (10, 7): 'mountain',
            (10, 8): 'mountain', (10, 9): 'mountain', (10, 10): 'mountain',
            (10, 11): 'mountain', (10, 12): 'mountain', (10, 13): 'mountain',
            (10, 14): 'mountain', (10, 15): 'mountain', (10, 16): 'mountain',
            
            # Diagonal mountain ranges
            (5, 2): 'mountain', (6, 3): 'mountain', (7, 4): 'mountain',
            (5, 5): 'mountain', (6, 6): 'mountain', (7, 7): 'mountain',
            (13, 2): 'mountain', (14, 3): 'mountain', (15, 4): 'mountain',
            (13, 5): 'mountain', (14, 6): 'mountain', (15, 7): 'mountain',
            
            # Village clusters
            (3, 15): 'village', (4, 15): 'village', (3, 16): 'village',
            (16, 15): 'village', (17, 15): 'village', (16, 16): 'village',
            
            # Farmland maze
            (2, 2): 'farmland', (18, 2): 'farmland', 
            (2, 18): 'farmland', (18, 18): 'farmland',
            (5, 10): 'farmland', (15, 10): 'farmland',
            
            # Spiral mountain pattern
            (8, 8): 'mountain', (9, 8): 'mountain', (11, 8): 'mountain', (12, 8): 'mountain',
            (12, 9): 'mountain', (12, 10): 'mountain', (12, 11): 'mountain',
            (11, 11): 'mountain', (10, 11): 'mountain', (9, 11): 'mountain',
            (8, 11): 'mountain', (8, 10): 'mountain', (8, 9): 'mountain',
            
            # Protective village ring
            (5, 17): 'village', (15, 17): 'village',
            (7, 19): 'village', (13, 19): 'village',
            
            # Farmland traps near river
            (9, 1): 'farmland', (10, 1): 'farmland', (11, 1): 'farmland',
            
            # Bottom layer obstacles
            (0, 18): 'mountain', (19, 18): 'mountain',
            (1, 17): 'mountain',

            (18, 12): 'village'
        }
    }
]

villageCount = [1, 1, 9, 2, 1, 9, 16, 11]
fieldCount = [2, 4, 6, 2, 3, 6, 11, 9]

# --- Global variables for images and sounds ---
MOUNTAIN_IMG = None
VILLAGE_IMG = None
FARMLAND_IMG = None
CASTLE_IMG = None
SETUP_BG_IMG = None
GAME_BG_IMG = None
WIN_IMG = None
LOSE_IMG = None
LASTWIN_IMG = None
END_IMG = None

# Sound variables.
WATER_SOUND = None
WIN_SOUND = None
LOSE_SOUND = None
SOUND_CLICK = None
SOUND_VILLAGE = None
SOUND_FARMLAND = None
DRAW_SOUND = None
ERASE_SOUND = None
END_MUSIC = None