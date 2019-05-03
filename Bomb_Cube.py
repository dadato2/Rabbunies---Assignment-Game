from Object import *
from ScreenControl import ScreenController

cubeSprite = makeSprite("assets/3dCube.png", 48).images

class Cube(Object):

    def __init__(self):
        ObjectLists.listAllObjects.append(self)
        self.x = 0
        self.y = 0
        self.xy = (self.x, self.y)
        self.order = self.y
        self.height = 0
        self.maxHeight = 10
        self.thrown = False

        self.sprite = cubeSprite[0]
        self.spriteIndex = 0
        self.spriteIndexDelay = 0.4
        self.spriteIndexCounter = 0
        self.rect = self.sprite.get_rect()

    def animate(self):
        self.spriteIndexCounter += Time.deltaTime
        if self.spriteIndexCounter >= self.spriteIndexDelay:
            self.spriteIndexDelay = 0
            self.spriteIndex += 1
            self.spriteIndex %= 48

    def update(self):
        self.animate()

    def draw(self, screen):
        self.sprite = cubeSprite[self.spriteIndex]
        self.rect = self.sprite.get_rect()
        self.xy = (self.x-self.rect.center[0] + Constants.scr_shake_offset_x,
                   self.y-self.rect.center[1] + Constants.scr_shake_offset_y)
        if -self.rect.w < self.xy[0] < Constants.scr_width and -self.rect.h < self.xy[1] < Constants.scr_height:
            screen.blit(self.sprite, self.xy)
