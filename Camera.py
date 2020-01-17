from Constants import *
from functions import *


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        if -LEVEL_WIDTH <= obj.rect.x + self.dx <= 0:
            obj.rect.x += self.dx

    def update(self, target):
        # print(target.moving)
        self.dx = 0
        if target.moving[LEFT] != target.moving[RIGHT]:
            if target.moving[LEFT] == 1:
                self.dx = 1 * PLAYER_SPEED
            if target.moving[RIGHT] == 1:
                self.dx = -1 * PLAYER_SPEED

        # self.dx = -(target.rect.x + target.rect.w // 2 - 800 // 2)
        # self.dy = -(target.rect.y + target.rect.h // 2 - 600 // 2)


class Camera1:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.world_shift = 0

    def apply(self, obj):
        obj.rect[0] += self.dx

    def update(self, target):
        self.dx = 0

        # If the player gets near the right side, shift the world left (-x)
        if target.rect.x >= WIDTH - 120:
            diff = target.rect.x - 500
            target.rect.x = (WIDTH - 120)
            shift_world(self.world_shift, -diff)
            if self.world_shift - 120 > 0:
                if self.world_shift > 120:
                    self.world_shift += 120

        # If the player gets near the left side, shift the world right (+x)
        if target.rect.x <= 120:
            diff = 120 - target.rect.x
            target.rect.x = 120
            shift_world(self.world_shift, diff)
            if self.world_shift + 120 < LEVEL_WIDTH:
                if self.world_shift < WIDTH - 120:
                    self.world_shift -= 120


