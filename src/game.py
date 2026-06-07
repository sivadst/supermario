import pygame
from ..config.settings import *
from ..player.player import Player

class Game:
    """Main game class managing the game loop and player state."""

    def __init__(self):
        """Initialize the game and all game resources."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.Clock()
        self.player = Player(PLAYER_START_X, PLAYER_START_Y)
        self.running = True
        self.floor_y = SCREEN_HEIGHT - 50

    def handle_events(self):
        """Process all game events and update game state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False

    def update(self):
        """Update game objects and handle collisions."""
        self.player.handle_input()
        self.player.apply_gravity()
        self.player.move()

        # Floor collision
        if self.player.rect.bottom >= self.floor_y:
            self.player.rect.bottom = self.floor_y
            self.player.vel_y = 0
            self.player.on_ground = True
        else:
            self.player.on_ground = False

        # Keep player within screen bounds
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > SCREEN_WIDTH:
            self.player.rect.right = SCREEN_WIDTH
        if self.player.rect.top < 0:
            self.player.rect.top = 0

    def draw(self):
        """Render the game state to the screen."""
        self.screen.fill(SKY_BLUE)  # Background color

        # Draw floor
        pygame.draw.rect(self.screen, GREEN, (0, self.floor_y, SCREEN_WIDTH, SCREEN_HEIGHT - self.floor_y))

        # Draw player
        self.player.draw(self.screen)

        # Debug HUD
        font = pygame.font.SysFont(None, 18)
        y_offset = 10
        hud_text = [
            f"FPS: {self.clock.get_fps():.0f}",
            f"Pos: ({int(self.player.rect.x)}, {int(self.player.rect.y)})",
            f"Vel: ({self.player.vel_x:.1f}, {self.player.vel_y:.1f})",
            f"On Ground: {self.player.on_ground}"
        ]

        for text in hud_text:
            surf = font.render(text, True, WHITE)
            self.screen.blit(surf, (10, y_offset))
            y_offset += 20

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        print("Game initialized")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        print("Game closed")

    def cleanup(self):
        """Clean up game resources."""
        pygame.quit()