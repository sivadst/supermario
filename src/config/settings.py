import os

# Display Settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Super Mario Platformer"

# Color Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BROWN = (165, 42, 42)

# Physics Constants
GRAVITY = 0.8
JUMP_STRENGTH = -15
MOVE_SPEED = 5
MAX_FALL_SPEED = 15

# Player Settings
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 48
PLAYER_START_X = 100
PLAYER_START_Y = 300

# Tile System
TILE_SIZE = 32  # Must divide evenly into SCREEN dimensions

# World Settings
WORLD_WIDTH = 80  # tiles (80 * 32 = 2560 pixels wide world)
WORLD_HEIGHT = 24  # tiles (24 * 32 = 768 pixels tall)

# Tile Types (enum-style integers)
TILE_EMPTY = 0
TILE_GROUND = 1
TILE_BRICK = 2
TILE_QUESTION = 3  # coin block
TILE_PIPE_TOP = 4
TILE_PIPE_BODY = 5
TILE_HARD_BLOCK = 6

# Colors for tile types (placeholder until sprites)
TILE_COLORS = {
    TILE_EMPTY: None,  # transparent
    TILE_GROUND: (139, 69, 19),      # brown
    TILE_BRICK: (210, 105, 30),      # chocolate
    TILE_QUESTION: (255, 215, 0),    # gold
    TILE_PIPE_TOP: (34, 139, 34),    # forest green
    TILE_PIPE_BODY: (50, 205, 50),   # lime green
    TILE_HARD_BLOCK: (128, 128, 128) # gray
}

# Coin Settings
COIN_SIZE = 24
COIN_COLOR = (255, 223, 0)  # bright gold
COIN_VALUE = 100
COINS_PER_QUESTION_BLOCK = 1

# Score Settings
SCORE_FONT_SIZE = 24
SCORE_COLOR = (255, 255, 255)  # white
SCORE_POSITION = (20, 20)

# Camera Settings
CAMERA_SMOOTHING = 0.1  # lower = smoother follow (0.0 to 1.0)

# File Paths
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
PLAYER_ASSETS_DIR = os.path.join(ASSETS_DIR, 'player')
ENEMIES_ASSETS_DIR = os.path.join(ASSETS_DIR, 'enemies')
LEVELS_ASSETS_DIR = os.path.join(ASSETS_DIR, 'levels')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
SAVES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'saves')
CONFIG_DIR = os.path.dirname(__file__)