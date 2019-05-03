from Object import *
from bomb_explosion import Explosion
from ScreenControl import ScreenController

bombSprite = pygame.image.load("assets/Bomb.png")
bombSprite = pygame.transform.scale(bombSprite, (50, 50))

class Bomb(Object):
    def __init__(self):
        ObjectLists.listAllObjects.append(self)
        ObjectLists.listOfBombs.append(self)
        self.xpos = Global.player.xpos
        self.ypos = Global.player.ypos
        self.xy = (self.xpos, self.ypos)
        self.order = self.ypos
        self.height = 0
        self.scaler = 50
        self.maxHeight = 1
        self.thrown = False
        self.spriteOrigin = bombSprite
        self.scaledSpite = self.spriteOrigin
        self.sprite = self.spriteOrigin
        self.rect = self.sprite.get_rect()
        self.mouseButtonPressed = None

        self.explosionScale = 200
        self.direction = None
        self.fuse = 2
        self.fuseOriginal = self.fuse
        self.heightMultiplier = 30
        self.speed = 5
        self.target = None

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
            self.fuse = Global.Crosshair.distFromPLayer / 250 * Global.Crosshair.spriteScale/Global.Crosshair.scaleTime
            self.fuseOriginal = self.fuse
            self.thrown = True

        if not self.thrown:
            self.xpos, self.ypos = Global.player.xpos + 50, Global.player.ypos

        if self.thrown:
            self.fuse -= Time.deltaTime
            self.height = (self.fuseOriginal/2 - math.fabs((self.fuseOriginal/2) - self.fuse)) * self.heightMultiplier
            self.spriteOrigin = bombSprite
            self.scaledSpite = pygame.transform.scale(self.spriteOrigin, (int(self.scaler + self.height), int(self.scaler + self.height)))
            self.sprite = self.scaledSpite
            self.moveTowardTarget()
        self.rect = self.scaledSpite.get_rect()

        if self.fuse <= 0:
            Global.player.bombPresent = False
            newExpl = Explosion(self.xpos+self.rect.center[0], self.ypos+self.rect.center[1], self.explosionScale)
            Global.scr.shakeScreen(5, 0.3)
            ObjectLists.listOfBombs.remove(self)
            ObjectLists.listAllObjects.remove(self)
            del self
