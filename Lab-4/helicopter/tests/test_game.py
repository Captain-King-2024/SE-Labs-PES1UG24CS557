"""Deterministic headless checks; these do not replace manual gameplay."""

import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

from game.helicopter import Helicopter, MAX_VERTICAL_SPEED
from game.renderer import HEIGHT


def keys(up=False, down=False):
    return {pygame.K_UP: up, pygame.K_DOWN: down}


class MovementTests(unittest.TestCase):
    def test_prolonged_movement_stays_on_screen(self):
        for direction in (keys(up=True), keys(down=True)):
            helicopter = Helicopter(100, HEIGHT / 2)
            for _ in range(1000):
                helicopter.handle_input(direction)
                helicopter.update(HEIGHT)
                self.assertLessEqual(abs(helicopter.vy), MAX_VERTICAL_SPEED)
                self.assertGreaterEqual(helicopter.get_rect().top, 0)
                self.assertLessEqual(helicopter.get_rect().bottom, HEIGHT)
            self.assertEqual(helicopter.vy, 0)

    def test_speed_cap_and_immediate_reversals(self):
        helicopter = Helicopter(100, HEIGHT / 2)
        for _ in range(1000):
            helicopter.handle_input(keys(up=True))
        self.assertEqual(helicopter.vy, -MAX_VERTICAL_SPEED)
        helicopter.handle_input(keys(down=True))
        self.assertGreater(helicopter.vy, 0)
        for _ in range(1000):
            helicopter.handle_input(keys(down=True))
        self.assertEqual(helicopter.vy, MAX_VERTICAL_SPEED)
        helicopter.handle_input(keys(up=True))
        self.assertLess(helicopter.vy, 0)

    def test_reversal_moves_away_from_each_boundary(self):
        helicopter = Helicopter(100, 12)
        helicopter.handle_input(keys(down=True))
        helicopter.update(HEIGHT)
        self.assertGreater(helicopter.y, 12)
        helicopter.y = HEIGHT - 12
        helicopter.handle_input(keys(up=True))
        helicopter.update(HEIGHT)
        self.assertLess(helicopter.y, HEIGHT - 12)


if __name__ == "__main__":
    unittest.main()
