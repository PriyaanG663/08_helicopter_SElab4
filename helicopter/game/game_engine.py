"""
GameEngine: owns the helicopter and all obstacles.
"""

import random
import time
import pygame
from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3
SHIELD_COOLDOWN = 20.0


class GameEngine:
    def __init__(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.itime = int(time.time())
        
        # Shield properties
        self.shield_active = False
        self.last_shield_used_time = -99.0

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(margin + GAP_HEIGHT // 2, HEIGHT - margin - GAP_HEIGHT // 2)
        self.obstacles.append(Obstacle(
            x=WIDTH, gap_y=gap_y, gap_height=GAP_HEIGHT,
            wall_width=WALL_WIDTH, screen_height=HEIGHT, speed=SCROLL_SPEED,
        ))

    def handle_input(self, keys_pressed):
        self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if key == pygame.K_h:
            current_time = time.time()
            # Check if shield is not active and cooldown has passed
            if not self.shield_active and (current_time - self.last_shield_used_time >= SHIELD_COOLDOWN):
                self.shield_active = True

    def update(self):
        self.helicopter.update(HEIGHT)

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()
        
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        # Precise Collision Detection using Rects
        heli_rect = self.helicopter.get_rect()
        for obstacle in list(self.obstacles):
            if heli_rect.colliderect(obstacle.get_top_rect()) or heli_rect.colliderect(obstacle.get_bottom_rect()):
                if self.shield_active:
                    # Shield absorbs the hit and deactivates
                    self.shield_active = False
                    self.last_shield_used_time = time.time()
                    self.obstacles.remove(obstacle)
                else:
                    return False

        return True

    def draw(self, surface, font):
        from game import renderer
        current_time = time.time()
        cooldown_left = max(0.0, SHIELD_COOLDOWN - (current_time - self.last_shield_used_time))
        renderer.draw_scene(surface, self.helicopter, self.obstacles, self.shield_active, cooldown_left, font)

    def hope(self, surface, font):
        from game import renderer
        ftime = int(time.time())
        score = (ftime - self.itime) * SCROLL_SPEED
        renderer.draw_banner(surface, font, f"Points: {score}")