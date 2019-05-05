from Object import *
from bomb_explosion import Explosion
from ScreenControl import ScreenController


class Bomb(Object):
    def __init__(self, src):
        ObjectLists.listAllObjects.append(self)
        ObjectLists.listOfBombs.append(self)
        self.xpos = Global.player.xpos
        self.ypos = Global.player.ypos
        self.xy = (self.xpos, self.ypos)
        self.order = self.ypos
        self.height = 0
        self.scaler = 40
        self.maxHeight = 1
        self.thrown = False
        self.mouseButtonPressed = None
        self.direction = None
        self.fuse = 2
        self.fuseOriginal = self.fuse
        self.heightMultiplier = 30
        self.target = None

        self.source = src

        self.ignoreHeight = False

        self.explosionScale = 200
        self.speed = 5

        self.spriteOrigin = None
        self.scaledSpite = self.spriteOrigin
        self.sprite = self.spriteOrigin
        self.rect = None

    def moveTowardTarget(self):
        self.dirx = math.sin(self.direction) * self.speed
        self.diry = math.cos(self.direction) * self.speed

        self.xpos = int(self.xpos + self.dirx)
        self.ypos = int(self.ypos + self.diry)

    def update(self):
        self.mouseButtonPressed = pygame.mouse.get_pressed()[0]
        if not self.thrown and not self.mouseButtonPressed:
            self.target = Global.Crosshair.xy
            self.direction = GlobalMath.Angle(self, Global.Crosshair)
            self.fuse = Global.Crosshair.distFromPLayer / (50*self.speed) * Global.Crosshair.spriteScale/Global.Crosshair.scaleTime
            self.fuseOriginal = self.fuse
            self.xpos -= 50
            self.thrown = True

        if not self.thrown:
            self.xpos, self.ypos = Global.player.xpos + 25, Global.player.ypos

        if self.thrown:
            self.fuse -= Time.deltaTime
            self.height = (self.fuseOriginal/2 - math.fabs((self.fuseOriginal/2) - self.fuse)) * self.heightMultiplier
            # self.spriteOrigin = bombSprite
            if not self.ignoreHeight:
                self.scaledSpite = pygame.transform.scale(self.spriteOrigin,
                                                      (int(self.scaler + self.height), int(self.scaler + self.height)))
            self.sprite = self.scaledSpite
            self.moveTowardTarget()
        if not self.ignoreHeight:
            self.rect = self.sprite.get_rect()

        if self.fuse <= 0:
            self.source.bombPresent = False
            newExpl = Explosion(self.xpos+self.rect.center[0], self.ypos+self.rect.center[1], self.explosionScale)
            ObjectLists.listOfBombs.remove(self)
            ObjectLists.listAllObjects.remove(self)
            del self
