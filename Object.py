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
        self.rect = pygame.Rect(self.xpos, self.ypos, self.sprite.get_rect().w, self.sprite.get_rect().h)
        self.order = self.ypos - self.rect.h
        self.xy = (self.xpos - int(self.rect.w/2) + Constants.scr_shake_offset_x,
                   self.ypos - int(self.rect.h/2) + Constants.scr_shake_offset_y)
        if -self.rect.w < self.xy[0] < Constants.scr_width and -self.rect.h < self.xy[1] < Constants.scr_height:
            screen.blit(self.sprite, self.xy)
        if Global.Debug:
            pygame.draw.rect(screen, Colors.black, pygame.Rect(self.xpos-int(self.rect.w/2), self.ypos-int(self.rect.h/2), self.rect.w, self.rect.h), 1)
