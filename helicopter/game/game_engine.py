"""
GameEngine: owns the helicopter and all obstacles.
"""

import random
import time
from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3


class GameEngine:
    def __init__(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.itime = int(time.time())

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
        pass

    def update(self):
        self.helicopter.update(HEIGHT)

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()
        
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        # Collision Detection Logic
        for i in self.obstacles:
            # Check if helicopter is within the horizontal range of the obstacle wall
            h_left = self.helicopter.x
            h_right = self.helicopter.x + self.helicopter.width
            h_top = self.helicopter.y
            h_bottom = self.helicopter.y + self.helicopter.height

            if i.x < h_right and h_left < i.x + i.wall_width:
                top_wall_bottom = i.gap_y - i.gap_height / 2
                bottom_wall_top = i.gap_y + i.gap_height / 2

                # If any part of the helicopter hits the top or bottom wall
                if h_top < top_wall_bottom or h_bottom > bottom_wall_top:
                    return False

        return True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.helicopter, self.obstacles)

    def hope(self, surface, font):
        from game import renderer
        ftime = int(time.time())
        score = (ftime - self.itime) * SCROLL_SPEED
        renderer.draw_banner(surface, font, f"Points: {score}")