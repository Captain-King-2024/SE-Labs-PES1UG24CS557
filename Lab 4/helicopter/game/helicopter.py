"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.4
MAX_VERTICAL_SPEED = 6.0


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.0

    def handle_input(self, keys_pressed):
        direction = int(keys_pressed[pygame.K_DOWN]) - int(keys_pressed[pygame.K_UP])
        if direction:
            # Discard momentum in the old direction for an immediate reversal.
            if self.vy * direction < 0:
                self.vy = 0.0
            self.vy += direction * THRUST
        else:
            # Releasing the controls (or holding both) stops vertical movement.
            self.vy = 0.0
        self.vy = max(-MAX_VERTICAL_SPEED, min(MAX_VERTICAL_SPEED, self.vy))

    def update(self, height_bound):
        self.y += self.vy
        # y is the centre, so leave room for both halves of the helicopter.
        half_height = self.height / 2
        if self.y < half_height:
            self.y = half_height
            self.vy = 0
        elif self.y > height_bound - half_height:
            self.y = height_bound - half_height
            self.vy = 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
