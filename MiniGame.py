import os
import random

import pygame
import DialogLib
from Constants import *
from functions import *
from groups import *
import Values


width, height = WIDTH, HEIGHT


class Heart(pygame.sprite.Sprite):
    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно!!!
        super().__init__(group)
        self.button_pressed = {"W": False, "A": False, "S": False, "D": False, "Sp": False}
        self.image = pygame.transform.scale(load_image("heart.png"), (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2
        self.rect.y = height // 2

    def handle_events(self):
        self.button_pressed = {"W": False, "A": False, "S": False, "D": False}
        if pygame.key.get_pressed()[100]:
            self.button_pressed["D"] = True
        if pygame.key.get_pressed()[97]:
            self.button_pressed["A"] = True
        if pygame.key.get_pressed()[119]:
            self.button_pressed["W"] = True
        if pygame.key.get_pressed()[115]:
            self.button_pressed["S"] = True

    def update(self):
        self.handle_events()

        if self.button_pressed["W"]:
            self.rect.y -= 20
        if self.button_pressed["A"]:
            self.rect.x -= 20
        if self.button_pressed["S"]:
            self.rect.y += 20
        if self.button_pressed["D"]:
            self.rect.x += 20

        if self.rect.x > width:
            self.rect.x -= width
        if self.rect.x < 0:
            self.rect.x += width

        if self.rect.y > height:
            self.rect.y -= height
        if self.rect.y < 0:
            self.rect.y += height

        if pygame.sprite.spritecollideany(self, enemy_group):
            pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно!!!
        super().__init__(group)
        self.image = load_image("shuriken.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width)
        self.vx, self.vy = random.randint(5, 15), random.randint(5, 15)
        self.rect.y = random.randint(0, height)

    def update(self):
        if pygame.sprite.spritecollideany(self, MG_mp):
            # self.rect.x += random.randint(-100, 100)
            # self.rect.y += random.randint(-100, 100)
            self.kill()
            Values.InstantHP -= 5

        self.rect.x += self.vx
        if self.rect.x > width:
            self.rect.x -= width
        if self.rect.x < 0:
            self.rect.x += width

        self.rect.y += self.vy

        if self.rect.y > height:
            self.rect.y -= height
        if self.rect.y < 0:
            self.rect.y += height

class Katana(pygame.sprite.Sprite):
    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно!!!
        super().__init__(group)
        self.image = load_image("laser1.png")
        self.rect = self.image.get_rect()
        self.rect.x = width * 0.1
        self.vx = 10
        self.rect.y = HEIGHT * 0.7

    def update(self):
        print(self.rect.x)
        if self.rect.x >= width * 0.9:
            self.vx = -10
        elif self.rect.x <= width * 0.1:
            self.vx = 10
        self.rect.x += self.vx


class MiniGame:
    def __init__(self, screen):
        self.screen = screen
        self.status = ATTACK
        self.katana = Katana(MG_d)
        self.zahler = 0
        self.x = self.y = 0
        self.fon = load_image("demon_fon.png")
        self.button_pressed = {"W": False, "A": False, "S": False, "D": False, "Sp": False}
        self.groups_dict = {ATTACK: [MG_mp, MG_e], DEFENSE: [MG_d]}
        for i in range(15):
            Enemy(self.groups_dict[ATTACK][1])
        self.main_person = Heart(self.groups_dict[ATTACK])

        self.AvailableGroup = [self.groups_dict[self.status]]

    def handle_events(self):
        if pygame.key.get_pressed()[32]:
            self.button_pressed["Sp"] = True

    def update(self):
        x = y = 0
        if Values.InstantHP <= 0:
            self.status = DEAD

        if self.zahler >= 50:
            self.status = DEFENSE

        if self.status == ATTACK:
            self.attack()

        elif self.status == DEFENSE:
            self.defense()

        elif self.status == DEAD:
            self.dead()

        self.AvailableGroup = self.groups_dict[self.status]

    def attack(self):
        self.zahler += 1
        if self.button_pressed["W"]:
            self.main_person.rect.y -= HEART_SPEED

        if self.button_pressed["A"]:
            self.main_person.rect.x -= HEART_SPEED

        if self.button_pressed["S"]:
            self.main_person.rect.y += HEART_SPEED

        if self.button_pressed["D"]:
            self.main_person.rect.x += HEART_SPEED

        self.main_person.update()

    def dead(self):
        self.status = ATTACK
        self.screen.fill((0, 0, 0))
        Values.MINIGAME = False
        Values.GIRL = False

    def defense(self):

        pygame.draw.rect(self.screen, (255, 255, 255), (int(width * 0.1), int(height * 0.7), int(width * 0.8), 50), 0)
        pygame.draw.rect(self.screen, (100, 100, 100), (int(width * 0.1) + self.x, int(height * 0.7) - 15, 10, 80), 0)
        self.katana.update()