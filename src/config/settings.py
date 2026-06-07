import os

# Display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Super Mario Platformer"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BROWN = (139, 69, 19)

# Physics
GRAVITY = 0.8
JUMP_STRENGTH = -15
MOVE_SPEED = 5
MAX_FALL_SPEED = 15
ACCELERATION = 0.5
FRICTION = 0.85

# Player
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 48
PLAYER_START_X = 100
PLAYER_START_Y = 300

# Tile System
TILE_SIZE = 32
WORLD_WIDTH = 80
WORLD_HEIGHT = 24

# Tile Types
TILE_EMPTY = 0
TILE_GROUND = 1
TILE_BRICK = 2
TILE_QUESTION = 3
TILE_PIPE_TOP = 4
TILE_PIPE_BODY = 5
TILE_HARD_BLOCK = 6

TILE_COLORS = {
    TILE_EMPTY: None,
    TILE_GROUND: (139, 69, 19),
    TILE_BRICK: (210, 105, 30),
    TILE_QUESTION: (255, 215, 0),
    TILE_PIPE_TOP: (34, 139, 34),
    TILE_PIPE_BODY: (50, 205, 50),
    TILE_HARD_BLOCK: (128, 128, 128),
}

# Coin
COIN_SIZE = 24
COIN_COLOR = (255, 223, 0)
COIN_VALUE = 100
COINS_PER_QUESTION_BLOCK = 1

# Score
SCORE_FONT_SIZE = 24
SCORE_COLOR = (255, 255, 255)

# Camera
CAMERA_SMOOTHING = 0.1

# Enemy
GOOMBA_WIDTH = 32
GOOMBA_HEIGHT = 32
GOOMBA_SPEED = 1.5
GOOMBA_COLOR = (139, 69, 19)
GOOMBA_GRAVITY = 0.6

# Health
MAX_HEALTH = 3
INVINCIBILITY_FRAMES = 120
DAMAGE_FLASH_INTERVAL = 10
STARTING_LIVES = 3
LIFE_UP_SCORE = 10000

# Game States
STATE_MAIN_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3
STATE_LEVEL_COMPLETE = 4
STATE_VICTORY = 5

# Menu
MENU_BG_COLOR = (0, 0, 50)
MENU_TITLE_COLOR = (255, 215, 0)
MENU_OPTION_COLOR = (255, 255, 255)
MENU_SELECTED_COLOR = (255, 255, 0)
MENU_FONT_SIZE_LARGE = 64
MENU_FONT_SIZE_MEDIUM = 32
MENU_FONT_SIZE_SMALL = 24

# Level
MAX_LEVELS = 3
LEVEL_TRANSITION_TIME = 180
CHECKPOINT_FLAG_COLOR = (255, 255, 0)
CHECKPOINT_POLE_COLOR = (128, 128, 128)

LEVELS = [
    {
        'name': '1-1',
        'spawn': (100, 300),
        'checkpoints': [(40, 20)],
        'enemy_spawns': [(15, 20), (25, 18), (40, 20), (55, 20)],
        'end_x': 75,
    },
    {
        'name': '1-2',
        'spawn': (100, 200),
        'checkpoints': [(30, 18), (60, 15)],
        'enemy_spawns': [(10, 20), (20, 20), (35, 18), (50, 20), (65, 15)],
        'end_x': 75,
    },
    {
        'name': '1-3',
        'spawn': (100, 300),
        'checkpoints': [(25, 20), (50, 12)],
        'enemy_spawns': [(15, 20), (30, 18), (45, 20), (60, 15), (70, 20)],
        'end_x': 75,
    }
]

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
SAVES_DIR = os.path.join(BASE_DIR, 'saves')
