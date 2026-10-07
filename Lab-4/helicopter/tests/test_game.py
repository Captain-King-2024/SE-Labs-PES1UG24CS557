"""Deterministic headless checks; these do not replace manual gameplay."""

import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

from game.helicopter import Helicopter, MAX_VERTICAL_SPEED
from game.game_engine import GameEngine, SCROLL_SPEED
from game.obstacle import Obstacle
from game.renderer import HEIGHT, WINDOW_SIZE


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


class CollisionTests(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()
        self.engine.frames_until_spawn = 10000

    def wall_pair(self, x=100):
        return Obstacle(x, 250, 150, 60, HEIGHT, 3)

    def test_both_walls_end_game(self):
        for y in (100, 400):
            with self.subTest(y=y):
                self.setUp()
                self.engine.helicopter.y = y
                self.engine.obstacles = [self.wall_pair()]
                self.engine.update()
                self.assertTrue(self.engine.game_over)

    def test_gap_traversal_is_safe_at_different_heights(self):
        for y in (188, 250, 312):
            with self.subTest(y=y):
                self.setUp()
                self.engine.helicopter.y = y
                self.engine.obstacles = [self.wall_pair(x=150)]
                for _ in range(80):
                    self.engine.update()
                    self.assertFalse(self.engine.game_over)
                self.assertEqual(self.engine.obstacles, [])

    def test_game_over_freezes_world_and_input(self):
        self.engine.helicopter.y = 100
        obstacle = self.wall_pair()
        self.engine.obstacles = [obstacle]
        self.engine.update()
        before = (self.engine.helicopter.y, self.engine.helicopter.vy,
                  obstacle.x, self.engine.frames_until_spawn)
        for _ in range(100):
            self.engine.handle_input(keys(down=True))
            self.engine.update()
        self.assertEqual(before, (self.engine.helicopter.y, self.engine.helicopter.vy,
                                  obstacle.x, self.engine.frames_until_spawn))

    def test_restart_creates_fresh_state(self):
        old_helicopter = self.engine.helicopter
        self.engine.helicopter.y = 100
        self.engine.obstacles = [self.wall_pair()]
        self.engine.update()
        self.engine.handle_keydown(pygame.K_r)
        self.assertFalse(self.engine.game_over)
        self.assertIsNot(self.engine.helicopter, old_helicopter)
        self.assertEqual(self.engine.helicopter.y, HEIGHT / 2)
        self.assertEqual(self.engine.helicopter.vy, 0)
        self.assertEqual(self.engine.obstacles, [])
        self.assertEqual(self.engine.frames_until_spawn, 0)
        self.engine.update()
        self.assertEqual(len(self.engine.obstacles), 1)

    def test_game_over_renders_headlessly(self):
        pygame.font.init()
        self.engine.game_over = True
        self.engine.draw(pygame.Surface(WINDOW_SIZE), pygame.font.Font(None, 22))


class DistanceTests(unittest.TestCase):
    def test_distance_matches_world_scroll(self):
        engine = GameEngine()
        engine.frames_until_spawn = 10000
        obstacle = Obstacle(600, 250, 150, 60, HEIGHT, SCROLL_SPEED)
        engine.obstacles = [obstacle]
        for _ in range(60):
            engine.update()
        self.assertEqual(engine.distance, 600 - obstacle.x)
        self.assertEqual(engine.distance, 180)

    def test_empty_world_still_counts_distance(self):
        engine = GameEngine()
        engine.frames_until_spawn = 10000
        engine.update()
        self.assertEqual(engine.distance, SCROLL_SPEED)

    def test_final_distance_freezes_and_restart_resets(self):
        engine = GameEngine()
        engine.helicopter.y = 100
        engine.obstacles = [Obstacle(100, 250, 150, 60, HEIGHT, SCROLL_SPEED)]
        engine.update()
        self.assertTrue(engine.game_over)
        final_distance = engine.distance
        self.assertEqual(final_distance, SCROLL_SPEED)
        for _ in range(100):
            engine.update()
        self.assertEqual(engine.distance, final_distance)
        engine.handle_keydown(pygame.K_r)
        self.assertEqual(engine.distance, 0)
        engine.update()
        self.assertEqual(engine.distance, SCROLL_SPEED)


if __name__ == "__main__":
    unittest.main()
