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

# Tile Size (for future use)
TILE_SIZE = 32

# File Paths
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
PLAYER_ASSETS_DIR = os.path.join(ASSETS_DIR, 'player')
ENEMIES_ASSETS_DIR = os.path.join(ASSETS_DIR, 'enemies')
LEVELS_ASSETS_DIR = os.path.join(ASSETS_DIR, 'levels')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
SAVES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'saves')
CONFIG_DIR = os.path.dirname(__file__)
