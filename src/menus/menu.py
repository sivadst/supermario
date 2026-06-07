import pygame

from ..config.settings import *


class Menu:
    """Game menu system."""

    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont("arial", MENU_FONT_SIZE_LARGE)
        self.font_medium = pygame.font.SysFont("arial", MENU_FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.SysFont("arial", MENU_FONT_SIZE_SMALL)
        self.selected_index = 0
        self.options = []
        self.title = ""
        self.final_score = 0

    def set_main_menu(self):
        self.title = "SUPER MARIO PLATFORMER"
        self.options = ["Start Game", "Quit"]
        self.selected_index = 0

    def set_pause_menu(self):
        self.title = "PAUSED"
        self.options = ["Resume", "Restart Level", "Quit to Menu"]
        self.selected_index = 0

    def set_game_over_menu(self):
        self.title = "GAME OVER"
        self.options = ["Restart Level", "Quit to Menu"]
        self.selected_index = 0

    def set_victory_menu(self, score):
        self.title = "YOU WIN!"
        self.final_score = score
        self.options = ["Play Again", "Quit"]
        self.selected_index = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return self.options[self.selected_index].lower().replace(" ", "_")
                elif event.key == pygame.K_ESCAPE:
                    if any("resume" in option.lower() for option in self.options):
                        return "resume"
                    return "quit"
        return None

    def draw(self):
        self.screen.fill(MENU_BG_COLOR)

        title_surf = self.font_large.render(self.title, True, MENU_TITLE_COLOR)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)

        if self.final_score > 0 and "YOU WIN" in self.title:
            score_surf = self.font_medium.render(
                f"Final Score: {self.final_score:06d}",
                True,
                MENU_OPTION_COLOR,
            )
            score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 240))
            self.screen.blit(score_surf, score_rect)

        start_y = 320
        for i, option in enumerate(self.options):
            color = MENU_SELECTED_COLOR if i == self.selected_index else MENU_OPTION_COLOR
            text = f"> {option} <" if i == self.selected_index else option
            surf = self.font_medium.render(text, True, color)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 60))
            self.screen.blit(surf, rect)

        inst = self.font_small.render(
            "UP/DOWN to select, ENTER to confirm",
            True,
            (200, 200, 200),
        )
        inst_rect = inst.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        self.screen.blit(inst, inst_rect)

        pygame.display.flip()
