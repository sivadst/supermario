import pygame

from ..config.settings import *


class Camera:
    """Camera with Mario-style dead zone and smooth follow."""

    def __init__(self, width, height, world_width, world_height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        self.dead_zone = width // 3

    def follow(self, target_rect):
        desired_x = target_rect.centerx - self.width // 2
        desired_y = target_rect.centery - self.height // 2

        if target_rect.centerx > self.offset.x + self.dead_zone:
            desired_x = target_rect.centerx - self.dead_zone

        desired_x = max(0, min(desired_x, self.world_width - self.width))
        desired_y = max(0, min(desired_y, self.world_height - self.height))

        self.offset.x += (desired_x - self.offset.x) * CAMERA_SMOOTHING
        self.offset.y += (desired_y - self.offset.y) * CAMERA_SMOOTHING

    def apply(self, rect):
        if isinstance(rect, pygame.Rect):
            return pygame.Rect(
                rect.x - self.offset.x,
                rect.y - self.offset.y,
                rect.w,
                rect.h,
            )
        return (rect[0] - self.offset.x, rect[1] - self.offset.y)

    def is_visible(self, rect):
        return rect.colliderect(
            pygame.Rect(self.offset.x, self.offset.y, self.width, self.height)
        )
