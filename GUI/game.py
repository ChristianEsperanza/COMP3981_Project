import pygame
from Utility.constants import *


class Game:
    """
    The Game class is the driver of the Abalone game. It initiates
    the setup to open a window and run the game.
    """

    def __init__(self):
        pass

    def run(self):
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Abalone")
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                self.handle_click(event)
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit()

    def set_up_board(self):
        pass
