from Object import *
from bomb_explosion import Explosion
from ScreenControl import ScreenController


class Bomb(Object):
    def __init__(self, src):
        ObjectLists.listAllObjects.append(self) # add self to main object lists
        ObjectLists.listOfBombs.append(self)
        # position and size, etc.
        self.xpos = src.xpos
        self.ypos = src.ypos
        self.xy = (self.xpos, self.ypos)
        self.order = self.ypos
        self.height = 0
        self.scaler = 40
        self.maxHeight = 1
        self.thrown = False
        self.mouseButtonPressed = None
        self.direction = None # in angles
        self.fuse = 2 # how long left until explode
        self.fuseOriginal = self.fuse  # to keep track of how long it's been alive
        self.heightMultiplier = 30  # increase/decrease this for the height effect
        self.target = None   # target coordinates (x, y)

        self.source = src  # the enemy or player that threw the bomb

        self.ignoreHeight = False  # used for the 3d cube since it's an animation and this saves time

        self.explosionScale = 200   # the size of the explosion
        self.speed = 5  # speed of movement

        self.spriteOrigin = None    # the origin sprite
        self.scaledSpite = self.spriteOrigin  # sprite after scaling
        self.sprite = self.spriteOrigin  # final sprite, to be drawn
        self.rect = None  # rect

    def moveTowardTarget(self):  # to move toward target
        self.dirx = math.sin(self.direction) * self.speed  # this code I learned in class
        self.diry = math.cos(self.direction) * self.speed  # direction is in angles

        self.xpos = int(self.xpos + self.dirx)
        self.ypos = int(self.ypos + self.diry)

    def update(self):
        self.mouseButtonPressed = pygame.mouse.get_pressed()[0]
        if not self.thrown and not self.mouseButtonPressed:   # when player releases mouse button, shoots the bomb, this happens only once
            self.target = Global.Crosshair.xy   # target coorfinates
            self.direction = GlobalMath.Angle(self, Global.Crosshair)
            self.fuse = Global.Crosshair.distFromPLayer / (50*self.speed) * Global.Crosshair.spriteScale/Global.Crosshair.scaleTime
            # makes it so that fuse is just enough to explode on the target coordinates ^
            self.fuseOriginal = self.fuse
            self.xpos -= 50   # sets position to original position
            self.thrown = True

        if not self.thrown:   # while the bomb is not thown, keep it next to the player
            self.xpos, self.ypos = Global.player.xpos + 25, Global.player.ypos

        if self.thrown:
            self.fuse -= Time.deltaTime
            self.height = (self.fuseOriginal/2 - math.fabs((self.fuseOriginal/2) - self.fuse)) * self.heightMultiplier
            # prevent negative scale
            if self.scaler < 0:
                self.scaler = 0
            if self.height < 0:
                self.height = 0
            if not self.ignoreHeight:   # scale the sprite based on height
                self.scaledSpite = pygame.transform.scale(self.spriteOrigin,
                                                      (int(self.scaler + self.height), int(self.scaler + self.height)))
            self.sprite = self.scaledSpite
            self.moveTowardTarget()

        if self.fuse <= 0:     # upon exploding
            self.source.bombPresent = False  # prevents player from throwig multiple bombs at once
            newExpl = Explosion(self.xpos+int(self.rect.w/2), self.ypos+int(self.rect.h/2), self.explosionScale)
            # creates the explosion from center of character sprite
            ObjectLists.listOfBombs.remove(self)
            ObjectLists.listAllObjects.remove(self)
            del self
            return
