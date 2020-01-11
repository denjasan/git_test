import os
import pygame
from Constants import *
from Player import *


class Main():
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.background = pygame.image.load('data/ClubNeon.png')
        self.main_loop()
        self.player = Player

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        """ rendering everything """
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def main_loop(self):
        """ main program cycle """
        while self.running:
            self.render()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    game = Main(screen)

