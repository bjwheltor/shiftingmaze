"""
Utilitu functions

History
08-Jan-2022 - Initial module
"""
import sys
import pygame


def wait_for_exit():
    # wait for an exit for a pygame window
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    pygame.quit()
    sys.exit()
