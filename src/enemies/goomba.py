from ..config.settings import TILE_SIZE, WORLD_WIDTH
from .base_enemy import BaseEnemy


class Goomba(BaseEnemy):
    """Basic walking enemy."""

    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self, level, player_rect):
        if not self.alive:
            return
        self.apply_gravity()
        self.check_tile_collision(level)

        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x *= -1
            self.direction *= -1
        if self.rect.right > WORLD_WIDTH * TILE_SIZE:
            self.rect.right = WORLD_WIDTH * TILE_SIZE
            self.vel_x *= -1
            self.direction *= -1
