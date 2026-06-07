import pygame

from ..config.settings import *
from ..enemies.goomba import Goomba
from .checkpoint import Checkpoint


class Level:
    """Tile-based level with enemies, checkpoints, and coins."""

    def __init__(self, level_id=0, level_data=None):
        self.level_id = level_id
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT
        self.tiles = []
        self.coins = []
        self.collected_coins = set()
        self.question_blocks_hit = set()
        self.enemies = []
        self.checkpoints = []
        self.completed = False
        self.end_flag_x = 0

        data = level_data or LEVELS[level_id]
        self.name = data["name"]
        self.spawn = data["spawn"]
        self.end_flag_x = data["end_x"] * TILE_SIZE

        self.generate_level()
        self.create_checkpoints(data.get("checkpoints", []))
        self.spawn_enemies(data.get("enemy_spawns", []))
        self.build_surface()

    def generate_level(self):
        self.tiles = [[TILE_EMPTY for _ in range(self.width)] for _ in range(self.height)]

        for row in range(self.height - 2, self.height):
            for col in range(self.width):
                self.tiles[row][col] = TILE_GROUND

        if self.level_id == 0:
            self._add_platform(18, 10, 15, TILE_BRICK)
            self._add_platform(15, 20, 25, TILE_BRICK)
            self._add_platform(12, 30, 35, TILE_QUESTION)
            self._add_platform(16, 40, 42, TILE_HARD_BLOCK)
            self._add_pipe(50, 21)
            self._add_stairs(60, 5)
        elif self.level_id == 1:
            self._add_platform(14, 10, 18, TILE_BRICK)
            self._add_platform(10, 25, 30, TILE_BRICK)
            self._add_platform(16, 35, 40, TILE_QUESTION)
            self._add_platform(8, 50, 55, TILE_HARD_BLOCK)
            self._add_pipe(45, 21)
            self._add_stairs(65, 4)
        else:
            self._add_platform(12, 15, 22, TILE_BRICK)
            self._add_platform(8, 30, 38, TILE_BRICK)
            self._add_platform(15, 45, 50, TILE_QUESTION)
            self._add_platform(10, 55, 60, TILE_HARD_BLOCK)
            self._add_pipe(40, 21)
            self._add_stairs(70, 6)

    def _add_platform(self, row, col_start, col_end, tile_type):
        for col in range(col_start, col_end + 1):
            if 0 <= row < self.height and 0 <= col < self.width:
                self.tiles[row][col] = tile_type

    def _add_pipe(self, col, row):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.tiles[row][col] = TILE_PIPE_TOP
            if row + 1 < self.height:
                self.tiles[row + 1][col] = TILE_PIPE_BODY

    def _add_stairs(self, col_start, height):
        for i in range(height):
            for c in range(col_start + i, col_start + height):
                row = self.height - 3 - i
                if 0 <= row < self.height and 0 <= c < self.width:
                    self.tiles[row][c] = TILE_HARD_BLOCK

    def create_checkpoints(self, checkpoint_data):
        for tile_x, tile_y in checkpoint_data:
            self.checkpoints.append(Checkpoint(tile_x, tile_y))

    def spawn_enemies(self, enemy_data):
        for tile_x, tile_y in enemy_data:
            x = tile_x * TILE_SIZE
            y = tile_y * TILE_SIZE
            self.enemies.append(Goomba(x, y))

    def build_surface(self):
        self.surface = pygame.Surface((self.width * TILE_SIZE, self.height * TILE_SIZE))
        self.surface.fill(SKY_BLUE)
        for row in range(self.height):
            for col in range(self.width):
                tile = self.tiles[row][col]
                if tile != TILE_EMPTY and TILE_COLORS[tile]:
                    rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.surface, TILE_COLORS[tile], rect)
                    if tile == TILE_QUESTION and (row, col) not in self.question_blocks_hit:
                        pygame.draw.rect(self.surface, (200, 170, 0), rect, 2)

    def get_tile(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.tiles[row][col]
        return TILE_EMPTY

    def is_solid(self, row, col):
        tile = self.get_tile(row, col)
        return tile in (
            TILE_GROUND,
            TILE_BRICK,
            TILE_PIPE_TOP,
            TILE_PIPE_BODY,
            TILE_HARD_BLOCK,
            TILE_QUESTION,
        )

    def hit_question_block(self, row, col):
        if (row, col) not in self.question_blocks_hit and self.get_tile(row, col) == TILE_QUESTION:
            self.question_blocks_hit.add((row, col))
            coin_x = col * TILE_SIZE + (TILE_SIZE - COIN_SIZE) // 2
            coin_y = (row - 1) * TILE_SIZE + 4
            self.coins.append(pygame.Rect(coin_x, coin_y, COIN_SIZE, COIN_SIZE))
            self.build_surface()
            return True
        return False

    def get_tile_rect(self, row, col):
        return pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def get_solid_tiles_near(self, rect):
        tiles = []
        start_row = max(0, int(rect.top // TILE_SIZE) - 1)
        end_row = min(self.height, int(rect.bottom // TILE_SIZE) + 2)
        start_col = max(0, int(rect.left // TILE_SIZE) - 1)
        end_col = min(self.width, int(rect.right // TILE_SIZE) + 2)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if self.is_solid(row, col):
                    tiles.append((self.get_tile_rect(row, col), self.get_tile(row, col)))
        return tiles

    def collect_coin(self, coin_index):
        self.collected_coins.add(coin_index)

    def check_checkpoint_collision(self, player_rect):
        for i, checkpoint in enumerate(self.checkpoints):
            if not checkpoint.is_activated() and player_rect.colliderect(checkpoint.get_rect()):
                checkpoint.activate()
                return i, checkpoint
        return None

    def check_level_end(self, player_rect):
        return player_rect.right >= self.end_flag_x

    def update(self, player_rect):
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(self, player_rect)
        for checkpoint in self.checkpoints:
            checkpoint.update()

    def draw(self, surface, camera_offset):
        surface.blit(self.surface, (-camera_offset.x, -camera_offset.y))

        for row in range(self.height):
            for col in range(self.width):
                if self.tiles[row][col] == TILE_QUESTION and (row, col) not in self.question_blocks_hit:
                    rect = self.get_tile_rect(row, col)
                    draw_rect = rect.move(-camera_offset.x, -camera_offset.y)
                    pygame.draw.rect(surface, TILE_COLORS[TILE_QUESTION], draw_rect)
                    pygame.draw.rect(surface, (200, 170, 0), draw_rect, 2)

        for i, coin_rect in enumerate(self.coins):
            if i not in self.collected_coins:
                draw_rect = coin_rect.move(-camera_offset.x, -camera_offset.y)
                pygame.draw.circle(surface, COIN_COLOR, draw_rect.center, COIN_SIZE // 2)

        for checkpoint in self.checkpoints:
            checkpoint.draw(surface, camera_offset)

        flag_x = self.end_flag_x - camera_offset.x
        pygame.draw.rect(surface, CHECKPOINT_POLE_COLOR, (flag_x, 400, 8, 320))
        pygame.draw.polygon(
            surface,
            CHECKPOINT_FLAG_COLOR,
            [(flag_x + 8, 400), (flag_x + 32, 420), (flag_x + 8, 440)],
        )

        for enemy in self.enemies:
            enemy.draw(surface, camera_offset)

    def get_spawn_point(self):
        return self.spawn
