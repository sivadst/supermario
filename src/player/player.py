import pygame
from ..config.settings import *

class Player:
    """Player character with movement and physics."""
    
    def __init__(self, x: int, y: int):
        """Initialize player at position (x, y).
        
        Args:
            x: Initial x-coordinate
            y: Initial y-coordinate
        """
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.on_ground = False
        self.facing_right = True
        self.color = GOLD
        
    def handle_input(self):
        """Process keyboard input for movement and jumping."""
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -MOVE_SPEED
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = MOVE_SPEED
            self.facing_right = True
        else:
            self.vel_x = 0
            
        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.jump()
    
    def apply_gravity(self):
        """Apply gravity to vertical velocity."""
        if not self.on_ground:
            self.vel_y += GRAVITY
            if self.vel_y > MAX_FALL_SPEED:
                self.vel_y = MAX_FALL_SPEED
    
    def move(self):
        """Apply velocity to position and reset horizontal velocity."""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        # Reset horizontal velocity after applying (frictionless horizontal movement)
        self.vel_x = 0
    
    def jump(self):
        """Make the player jump if on ground."""
        self.vel_y = JUMP_STRENGTH
        self.on_ground = False
    
    def update(self):
        """Update player state: input, gravity, movement."""
        self.handle_input()
        self.apply_gravity()
        self.move()
    
    def draw(self, surface: pygame.Surface):
        """Draw the player on the given surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw main rectangle
        pygame.draw.rect(surface, self.color, self.rect)
        
        # Draw simple eyes to indicate direction
        eye_size = 4
        eye_offset_x = 8 if self.facing_right else self.rect.width - 12
        eye_offset_y = 10
        pygame.draw.circle(surface, BLACK, 
                         (self.rect.x + eye_offset_x, self.rect.y + eye_offset_y), 
                         eye_size)
        pygame.draw.circle(surface, BLACK, 
                         (self.rect.x + eye_offset_x + 8, self.rect.y + eye_offset_y), 
                         eye_size)
    
    def get_position(self) -> tuple:
        """Get the player's current position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return (self.rect.x, self.rect.y)
