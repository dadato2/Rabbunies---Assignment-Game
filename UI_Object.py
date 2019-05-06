from ExtClasses import *
from pygame_logic import makeSprite, newSprite


class UI_Object():   # similar to object class, but has less logic and is drawn on top
    def __init__(self):
        self.xpos = None
        self.ypos = None
        self.image = None
        self.layer = 0

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.xpos,self.ypos))