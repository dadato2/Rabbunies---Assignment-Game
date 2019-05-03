import pygame, random
from pygame.locals import *
import math
from ExtClasses import *
from pygame_logic import makeSprite, newSprite


class Object:
    def __init__(self):
        self.xpos = None
        self.ypos = None
        self.xy = None
        self.sprite = None
        self.order = None
        self.rect = None

    def update(self):
        pass

    def draw(self, screen):
        self.order = self.ypos - self.rect.h
        self.xy = (self.xpos - self.rect.center[0] + Constants.scr_shake_offset_x,
                   self.ypos - self.rect.center[1] + Constants.scr_shake_offset_y)
        if -self.rect.w < self.xy[0] < Constants.scr_width and -self.rect.h < self.xy[1] < Constants.scr_height:
            screen.blit(self.sprite, self.xy)
