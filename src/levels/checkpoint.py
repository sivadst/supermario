import pygame

from ..config.settings import *


class Checkpoint:
    """Checkpoint flag that activates when touched."""

    def __init__(self, tile_x, tile_y):
        self.rect = pygame.Rect(tile_x * TILE_SIZE, tile_y * TILE_SIZE - 48, 32, 48)
        self.pole_rect = pygame.Rect(
            tile_x * TILE_SIZE + 12,
            tile_y * TILE_SIZE - 48,
            8,
            48,
        )
        self.activated = False
        self.wave_timer = 0

    def activate(self):
        self.activated = True

    def is_activated(self):
        return self.activated

    def update(self):
        if self.activated:
            self.wave_timer += 1

    def draw(self, surface, camera_offset):
        pole_draw = self.pole_rect.move(-camera_offset.x, -camera_offset.y)
        pygame.draw.rect(surface, CHECKPOINT_POLE_COLOR, pole_draw)

        flag_color = CHECKPOINT_FLAG_COLOR if self.activated else (200, 200, 200)
        offset = 3 if self.activated and (self.wave_timer % 20 > 10) else 0

        points = [
            (self.rect.x + 20 - camera_offset.x, self.rect.y + offset - camera_offset.y),
            (self.rect.x + 32 - camera_offset.x, self.rect.y + 8 + offset - camera_offset.y),
            (self.rect.x + 20 - camera_offset.x, self.rect.y + 16 + offset - camera_offset.y),
        ]
        pygame.draw.polygon(surface, flag_color, points)

    def get_rect(self):
        return self.rect
