"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.4


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.0

    def handle_input(self, keys_pressed):
        if keys_pressed[pygame.K_UP]:
            if self.vy > -3 * THRUST:
                self.vy -= THRUST
        if keys_pressed[pygame.K_DOWN]:
            if self.vy < 3 * THRUST:
                self.vy += THRUST

    def update(self, height_bound):
        self.y += self.vy
        if self.y - self.height / 2 < 0:
            self.y = self.height / 2
            self.vy = 0
        if self.y + self.height / 2 > height_bound:
            self.y = height_bound - self.height / 2
            self.vy = 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )