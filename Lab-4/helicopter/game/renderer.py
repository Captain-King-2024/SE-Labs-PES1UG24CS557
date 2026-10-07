"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (140, 200, 230)
COLOR_HELI = (60, 60, 70)
COLOR_OBSTACLE = (70, 150, 80)
COLOR_TEXT = (20, 20, 20)
COLOR_SHIELD = (0, 70, 220)


def draw_scene(surface, helicopter, obstacles, shield_active=False):
    surface.fill(COLOR_BG)
    for obstacle in obstacles:
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_top_rect())
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_bottom_rect())
    pygame.draw.rect(surface, COLOR_HELI, helicopter.get_rect(), border_radius=4)
    if shield_active:
        radius = int(max(helicopter.width, helicopter.height) / 2) + 10
        pygame.draw.circle(surface, COLOR_SHIELD, helicopter.get_rect().center, radius, 3)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (180, 40, 40))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)


def draw_game_over(surface, font, distance):
    panel = pygame.Rect(100, HEIGHT // 2 - 65, WIDTH - 200, 150)
    pygame.draw.rect(surface, (245, 245, 245), panel, border_radius=10)
    draw_banner(surface, font, "Game Over")
    final_score = font.render(f"Final distance: {distance} px", True, COLOR_TEXT)
    surface.blit(final_score, final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 35)))
    restart = font.render("Press R to restart", True, COLOR_TEXT)
    surface.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))
