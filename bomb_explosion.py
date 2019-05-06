from Object import *

explosionSprite = makeSprite("assets/explosion.png", 12).images

class Explosion (Object):
    def __init__(self, xpos, ypos, scale):
        self.xpos, self.ypos = xpos, ypos
        self.order = Constants.scr_height
        ObjectLists.listAllObjects.append(self)
        ObjectLists.listOfExplosions.append(self)
        self.spriteImages = explosionSprite
        self.scale = scale   # scales the explosion based on bomb type
        self.scaleImages()
        self.spriteIndex = 0
        self.spriteDelay = 0.1  # variables for animation
        self.spriteTimer = 0
        self.sprite = self.spriteImages[0]
        self.rect = pygame.Rect(self.xpos - self.sprite.get_rect().w / 2, self.ypos - self.sprite.get_rect().h / 2,
                                self.sprite.get_rect().w, self.sprite.get_rect().h)
        Global.scr.shakeScreen(scale*.05, scale*0.002)  # shake the screen based on how big the explosion is

    def scaleImages(self):
        for i in range(0, 12):
            self.spriteImages[i] = pygame.transform.scale(self.spriteImages[i], (self.scale, self.scale))


    def update(self):
        self.order = self.ypos + 1000
        self.spriteTimer += Time.deltaTime
        if self.spriteTimer >= self.spriteDelay and self.spriteIndex < 11: # animate explosion, no loop
            self.spriteTimer = 0
            self.spriteIndex += 1

        self.sprite = self.spriteImages[self.spriteIndex]
        if self.spriteIndex >= 11:
            ObjectLists.listOfExplosions.remove(self)
            ObjectLists.listAllObjects.remove(self)
            del self
            return

    def draw(self, screen):
        super().draw(screen)
        self.order = Constants.scr_height  # draw the explosion on top of all sprites