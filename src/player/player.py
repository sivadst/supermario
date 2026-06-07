import pygame

from ..config.settings import *


class Player:
    """Player character with movement, physics, health, and lives."""

    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.on_ground = False
        self.facing_right = True
        self.level = None
        self.score = 0
        self.coins_collected = 0
        self.health = MAX_HEALTH
        self.lives = STARTING_LIVES
        self.invincible = False
        self.invincibility_timer = 0
        self.flash_timer = 0
        self.dead = False
        self.current_checkpoint = None
        self.level_complete = False
        self.lives_awarded = 0

    def set_level(self, level):
        self.level = level

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x -= ACCELERATION
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x += ACCELERATION
            self.facing_right = True

        self.vel_x = max(-MOVE_SPEED, min(MOVE_SPEED, self.vel_x))

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.jump()

    def apply_friction(self):
        keys = pygame.key.get_pressed()
        if not (
            keys[pygame.K_LEFT]
            or keys[pygame.K_RIGHT]
            or keys[pygame.K_a]
            or keys[pygame.K_d]
        ):
            self.vel_x *= FRICTION
            if abs(self.vel_x) < 0.1:
                self.vel_x = 0

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

    def apply_movement(self):
        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)

    def jump(self):
        self.vel_y = JUMP_STRENGTH
        self.on_ground = False

    def check_tile_collisions(self):
        if not self.level:
            return

        for tile_rect, _ in self.level.get_solid_tiles_near(self.rect):
            if self.rect.colliderect(tile_rect):
                if self.vel_x > 0:
                    self.rect.right = tile_rect.left
                    self.vel_x = 0
                elif self.vel_x < 0:
                    self.rect.left = tile_rect.right
                    self.vel_x = 0
                break

        self.on_ground = False
        for tile_rect, tile_type in self.level.get_solid_tiles_near(self.rect):
            if self.rect.colliderect(tile_rect):
                if self.vel_y > 0:
                    self.rect.bottom = tile_rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = tile_rect.bottom
                    self.vel_y = 0
                    if tile_type == TILE_QUESTION:
                        self.level.hit_question_block(
                            int(tile_rect.y // TILE_SIZE),
                            int(tile_rect.x // TILE_SIZE),
                        )
                break

    def check_coin_collisions(self):
        if not self.level:
            return
        for i, coin_rect in enumerate(self.level.coins):
            if i not in self.level.collected_coins and self.rect.colliderect(coin_rect):
                self.level.collect_coin(i)
                self.coins_collected += 1
                self.add_score(COIN_VALUE)

    def check_enemy_collisions(self, enemies):
        if self.dead or self.invincible:
            return
        for enemy in enemies:
            if not enemy.alive:
                continue
            if self.rect.colliderect(enemy.rect):
                if self.vel_y > 0 and self.rect.bottom <= enemy.rect.centery:
                    enemy.die()
                    self.vel_y = JUMP_STRENGTH * 0.6
                    self.add_score(200)
                else:
                    self.take_damage()

    def take_damage(self):
        if self.invincible or self.dead:
            return
        self.health -= 1
        if self.health <= 0:
            self.lose_life()
        else:
            self.invincible = True
            self.invincibility_timer = INVINCIBILITY_FRAMES

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.dead = True
        else:
            self.health = MAX_HEALTH
            self.invincible = False
            self.invincibility_timer = 0
            checkpoint = self.get_checkpoint()
            self.rect.x = checkpoint[0]
            self.rect.y = checkpoint[1]
            self.vel_x = 0
            self.vel_y = 0

    def add_score(self, points):
        self.score += points
        new_lives = self.score // LIFE_UP_SCORE
        if new_lives > self.lives_awarded:
            self.lives += new_lives - self.lives_awarded
            self.lives_awarded = new_lives

    def update_invincibility(self):
        if self.invincible:
            self.invincibility_timer -= 1
            self.flash_timer = (self.flash_timer + 1) % DAMAGE_FLASH_INTERVAL
            if self.invincibility_timer <= 0:
                self.invincible = False
                self.flash_timer = 0

    def check_bounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.right > WORLD_WIDTH * TILE_SIZE:
            self.rect.right = WORLD_WIDTH * TILE_SIZE
            self.vel_x = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
        if self.rect.top > WORLD_HEIGHT * TILE_SIZE:
            self.lose_life()

    def set_checkpoint(self, x, y):
        self.current_checkpoint = (x, y)

    def get_checkpoint(self):
        return self.current_checkpoint or (PLAYER_START_X, PLAYER_START_Y)

    def reset_for_new_level(self, spawn_x, spawn_y):
        self.rect.x = spawn_x
        self.rect.y = spawn_y
        self.vel_x = 0
        self.vel_y = 0
        self.health = MAX_HEALTH
        self.invincible = False
        self.invincibility_timer = 0
        self.flash_timer = 0
        self.dead = False
        self.current_checkpoint = None

    def reset_full(self):
        self.score = 0
        self.coins_collected = 0
        self.health = MAX_HEALTH
        self.lives = STARTING_LIVES
        self.invincible = False
        self.invincibility_timer = 0
        self.flash_timer = 0
        self.dead = False
        self.current_checkpoint = None
        self.lives_awarded = 0
        self.rect.x = PLAYER_START_X
        self.rect.y = PLAYER_START_Y
        self.vel_x = 0
        self.vel_y = 0

    def update(self, enemies=None):
        if self.dead:
            return
        self.handle_input()
        self.apply_friction()
        self.apply_gravity()
        self.apply_movement()
        self.check_tile_collisions()
        self.check_coin_collisions()
        if enemies:
            self.check_enemy_collisions(enemies)
        self.update_invincibility()
        self.check_bounds()

    def draw(self, surface, camera_offset):
        if self.dead:
            return
        if self.invincible and self.flash_timer < DAMAGE_FLASH_INTERVAL // 2:
            return

        draw_rect = self.rect.move(-camera_offset.x, -camera_offset.y)
        pygame.draw.rect(surface, GOLD, draw_rect)

        eye_y = draw_rect.centery - 8
        if self.facing_right:
            pygame.draw.circle(surface, WHITE, (draw_rect.centerx + 6, eye_y), 4)
            pygame.draw.circle(surface, BLACK, (draw_rect.centerx + 8, eye_y), 2)
        else:
            pygame.draw.circle(surface, WHITE, (draw_rect.centerx - 6, eye_y), 4)
            pygame.draw.circle(surface, BLACK, (draw_rect.centerx - 8, eye_y), 2)

    def get_position(self):
        return (self.rect.x, self.rect.y)
