"""
Helicopter Game (Lab Starter)

Run with:  python3 main.py

Controls: Up/Down arrows to move, H to activate Shield.
"""

import pygame
import time
from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Helicopter")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    running = True
    while running:
        # Initialize a fresh engine for each game session
        engine = GameEngine()
        game_over = False

        # --- Main Gameplay Loop ---
        while running and not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    engine.handle_keydown(event.key)

            keys = pygame.key.get_pressed()
            engine.handle_input(keys)
            
            # engine.update() returns False when the game terminates
            if engine.update() is False:
                game_over = True

            engine.draw(screen, font)
            pygame.display.flip()
            clock.tick(60)

        # --- Game Over / Wait for Key Press Loop ---
        if running:
            engine.hope(screen, font)
            pygame.display.flip()

            waiting_for_key = True
            while running and waiting_for_key:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_key = False
                    elif event.type == pygame.KEYDOWN:
                        # User pressed any key, restart game
                        waiting_for_key = False

                clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()