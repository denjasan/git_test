import os
import time

import pygame

from Constants import *
from Player import *
from functions import *
from game_area import *
from groups import *
from Camera import Camera


class Background(pygame.sprite.Sprite):
    def __init__(self, flag=False):
        super().__init__(all_sprites)
        self.image = load_image("ClubNeon.png")
        self.rect = self.image.get_rect()
        if not flag:
            self.rect.x = 0
        else:
            self.rect.x = -215
        self.rect.y = 117
        self.add(fon_group)


class Fon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("ZEROposter.jpg")
        self.rect = self.image.get_rect()
        self.rect = -200, 0
        self.add(fon_group)


class Loading(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("pause.png")
        self.rect = self.image.get_rect()
        self.rect = -200, 0
        self.add(fon_group)


class Main:
    def __init__(self, screen):

        self.clock = pygame.time.Clock()
        self.screen = screen
        self.stairs_del = None  # which coord we should del
        self.running = True
        self.background = Background()
        self.player = Player('Sosiska', ZERO)
        self.area = AreaY1()
        self.area_x = AreaX1()
        self.camera = Camera()

        pygame.mixer.init()
        pygame.mixer.music.load('data/music/start.ogg')
        pygame.mixer.music.play()

        self.fon = Fon()
        self.start_screen()
        self.fon.kill()

        pygame.mixer.music.load('data/music/club.ogg')
        pygame.mixer.music.play()

        self.pause = Loading()
        self.loading()
        self.pause.kill()
        self.screen.fill((0, 0, 0))

        self.main_loop()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.moving[RIGHT] = 1
                if event.key == pygame.K_a:
                    self.player.moving[LEFT] = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.player.moving[RIGHT] = 0
                if event.key == pygame.K_a:
                    self.player.moving[LEFT] = 0

    def render(self):
        """ rendering everything """
        self.player.render()
        all_sprites.update(self.area, self.area_x, self.stairs_del)
        all_sprites.draw(self.screen)

        player_group.update(self.area, self.area_x)
        player_group.draw(screen)

        # player_group.update(self.x, self.area)
        # self.x = 0
        # player_group.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.flip()

    def start_screen(self):
        """ start screen loop """

        all_sprites.draw(self.screen)

        intro_text = "PRESS ANY KEY TO START"
        font = pygame.font.Font(None, 40)
        string_rendered = font.render(intro_text, 1, pygame.Color('pink'))
        intro_rect = string_rendered.get_rect()
        text_w = string_rendered.get_width()
        text_h = string_rendered.get_height()
        intro_rect.y = 630
        intro_rect.x = (WIDTH - text_w) // 2
        pygame.draw.rect(self.screen, (0, 0, 0), (intro_rect.x - 10, intro_rect.y - 10, text_w + 20, text_h + 20), 0)
        pygame.draw.rect(self.screen, (255, 0, 0), (intro_rect.x - 10, intro_rect.y - 10, text_w + 20, text_h + 20), 1)
        self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(FPS)

    def loading(self):
        all_sprites.draw(self.screen)

        flag = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            if flag:
                return  # начинаем игру
            pygame.display.flip()
            # time.sleep(13.8)
            flag = True

    def main_loop(self):
        """ main program cycle """

        first_time = True
        while self.running:
            if self.player.state != DEAD:
                self.player.move()
            if self.player.rect.y < SECOND_FLOOR and first_time:
                self.area.kill()
                self.background.kill()
                self.area_x.kill()
                self.area = AreaY2()
                self.background = Background(True)
                self.area_x = AreaX1(True)
                first_time = False
                self.stairs_del = (55, 190, LEFT)
            self.render()
            self.handle_events()
            self.camera.update(self.player)
            # for i in fon_group:
            self.camera.apply(fon_group, self.player)
            # all_sprites.remove(player_group, self.area_x, self.area)
        terminate()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    # screen = pygame.display.set_mode((1920, 1080))
    game = Main(screen)
    game.main_loop()


