import pygame
from abc import ABC, abstractmethod

from ..config.settings import *


class BaseEnemy(ABC):
    """Abstract base class for all enemies."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, GOOMBA_WIDTH, GOOMBA_HEIGHT)
        self.vel_x = -GOOMBA_SPEED
        self.vel_y = 0
        self.alive = True
        self.on_ground = False
        self.direction = -1

    @abstractmethod
    def update(self, level, player_rect):
        pass

    def apply_gravity(self):
        self.vel_y += GOOMBA_GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

    def check_tile_collision(self, level):
        self.rect.x += int(self.vel_x)
        for tile_rect, _ in level.get_solid_tiles_near(self.rect):
            if self.rect.colliderect(tile_rect):
                if self.vel_x > 0:
                    self.rect.right = tile_rect.left
                elif self.vel_x < 0:
                    self.rect.left = tile_rect.right
                self.vel_x *= -1
                self.direction *= -1
                break

        self.rect.y += int(self.vel_y)
        self.on_ground = False
        for tile_rect, _ in level.get_solid_tiles_near(self.rect):
            if self.rect.colliderect(tile_rect):
                if self.vel_y > 0:
                    self.rect.bottom = tile_rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = tile_rect.bottom
                    self.vel_y = 0
                break

    def draw(self, surface, camera_offset):
        if not self.alive:
            return
        draw_rect = self.rect.move(-camera_offset.x, -camera_offset.y)
        pygame.draw.rect(surface, GOOMBA_COLOR, draw_rect)
        eye_y = draw_rect.centery - 4
        eye_x = draw_rect.centerx + (6 if self.direction == 1 else -6)
        pygame.draw.circle(surface, WHITE, (eye_x, eye_y), 3)
        pygame.draw.circle(surface, BLACK, (eye_x, eye_y), 1)

    def die(self):
        self.alive = False

    def get_rect(self):
        return self.rect
