import pygame

from .config.settings import *
from .levels.camera import Camera
from .levels.level import Level
from .menus.menu import Menu
from .player.player import Player


class Game:
    """Main game class managing all states and game loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", SCORE_FONT_SIZE)
        self.running = True
        self.game_state = STATE_MAIN_MENU
        self.menu = Menu(self.screen)
        self.menu.set_main_menu()
        self.current_level_id = 0
        self.level = None
        self.player = None
        self.camera = None
        self.level_transition_timer = 0
        self.checkpoint_message = ""
        self.message_timer = 0

    def start_level(self, level_id):
        if not (0 <= level_id < MAX_LEVELS):
            self.game_state = STATE_VICTORY
            self.menu.set_victory_menu(self.player.score if self.player else 0)
            return

        self.current_level_id = level_id
        self.level = Level(level_id)

        spawn = self.level.get_spawn_point()
        if self.player:
            self.player.reset_for_new_level(spawn[0], spawn[1])
            self.player.set_level(self.level)
        else:
            self.player = Player(spawn[0], spawn[1])
            self.player.set_level(self.level)

        self.camera = Camera(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            WORLD_WIDTH * TILE_SIZE,
            WORLD_HEIGHT * TILE_SIZE,
        )
        self.game_state = STATE_PLAYING
        self.level_transition_timer = 0
        self.checkpoint_message = ""
        self.message_timer = 0

    def next_level(self):
        self.start_level(self.current_level_id + 1)

    def restart_level(self):
        self.start_level(self.current_level_id)

    def return_to_main_menu(self):
        self.game_state = STATE_MAIN_MENU
        self.menu.set_main_menu()
        self.player = None
        self.level = None
        self.camera = None

    def handle_menu_action(self, action):
        if action == "start_game" or action == "play_again":
            self.player = Player(PLAYER_START_X, PLAYER_START_Y)
            self.start_level(0)
        elif action == "resume":
            self.game_state = STATE_PLAYING
        elif action == "restart_level":
            self.restart_level()
        elif action == "quit_to_menu":
            self.return_to_main_menu()
        elif action == "quit":
            if self.game_state == STATE_MAIN_MENU or self.game_state == STATE_VICTORY:
                self.running = False
            else:
                self.return_to_main_menu()

    def handle_events(self):
        if self.game_state in (
            STATE_MAIN_MENU,
            STATE_PAUSED,
            STATE_GAME_OVER,
            STATE_VICTORY,
        ):
            action = self.menu.handle_input()
            if action:
                self.handle_menu_action(action)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p and self.game_state == STATE_PLAYING:
                    self.game_state = STATE_PAUSED
                    self.menu.set_pause_menu()
                elif event.key == pygame.K_r and self.game_state == STATE_GAME_OVER:
                    self.restart_level()

    def update(self):
        if self.game_state != STATE_PLAYING:
            return

        self.level.update(self.player.rect)
        self.player.update(self.level.enemies)
        self.camera.follow(self.player.rect)

        result = self.level.check_checkpoint_collision(self.player.rect)
        if result:
            _, checkpoint = result
            self.player.set_checkpoint(checkpoint.rect.x, checkpoint.rect.y - PLAYER_HEIGHT)
            self.checkpoint_message = "CHECKPOINT!"
            self.message_timer = 120

        if self.level.check_level_end(self.player.rect):
            self.game_state = STATE_LEVEL_COMPLETE
            self.level_transition_timer = LEVEL_TRANSITION_TIME

        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.checkpoint_message = ""

        if self.player.dead:
            self.game_state = STATE_GAME_OVER
            self.menu.set_game_over_menu()

    def draw(self):
        if self.game_state in (STATE_MAIN_MENU, STATE_PAUSED, STATE_GAME_OVER, STATE_VICTORY):
            self.menu.draw()
            return

        self.screen.fill(SKY_BLUE)

        if self.level:
            self.level.draw(self.screen, self.camera.offset)

        if self.player:
            self.player.draw(self.screen, self.camera.offset)

        self.draw_hud()

        if self.game_state == STATE_LEVEL_COMPLETE:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            text = self.font.render("LEVEL COMPLETE!", True, GOLD)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, rect)
            self.level_transition_timer -= 1
            if self.level_transition_timer <= 0:
                self.next_level()

        pygame.display.flip()

    def draw_hud(self):
        if not self.player:
            return

        score_text = self.font.render(f"SCORE: {self.player.score:06d}", True, SCORE_COLOR)
        self.screen.blit(score_text, (20, 20))

        world_text = self.font.render(
            f"WORLD {self.level.name if self.level else '1-1'}",
            True,
            SCORE_COLOR,
        )
        world_rect = world_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(world_text, world_rect)

        coin_text = self.font.render(f"x{self.player.coins_collected:02d}", True, COIN_COLOR)
        self.screen.blit(coin_text, (SCREEN_WIDTH - 100, 20))
        pygame.draw.circle(self.screen, COIN_COLOR, (SCREEN_WIDTH - 120, 32), 8)

        for i in range(self.player.health):
            pygame.draw.circle(self.screen, RED, (20 + i * 30, 60), 10)

        lives_text = self.font.render(f"x{self.player.lives}", True, SCORE_COLOR)
        self.screen.blit(lives_text, (120, 55))

        if self.checkpoint_message:
            msg = self.font.render(self.checkpoint_message, True, GOLD)
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(msg, msg_rect)

        fps = int(self.clock.get_fps())
        debug = self.font.render(
            f"FPS:{fps} Pos:({self.player.rect.x},{self.player.rect.y}) "
            f"Vel:({self.player.vel_x:.1f},{self.player.vel_y:.1f}) "
            f"Ground:{self.player.on_ground}",
            True,
            (255, 255, 0),
        )
        self.screen.blit(debug, (20, SCREEN_HEIGHT - 30))

    def run(self):
        print("Game initialized")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        print("Game closed")

    def cleanup(self):
        pygame.quit()
