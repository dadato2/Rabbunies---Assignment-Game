from Object import *

explosionSprite = makeSprite("assets/explosion.png", 12).images

class Explosion (Object):
    def __init__(self, xpos, ypos, scale):
        self.xpos, self.ypos = xpos, ypos
        ObjectLists.listAllObjects.append(self)
        self.spriteImages = explosionSprite
        self.scale = scale
        self.scaleImages()
        self.spriteIndex = 0
        self.spriteDelay = 0.1
        self.spriteTimer = 0
        self.sprite = self.spriteImages[0]
        self.rect = self.sprite.get_rect()

    def scaleImages(self):
        for i in range(0, 12):
            self.spriteImages[i] = pygame.transform.scale(self.spriteImages[i], (self.scale, self.scale))


    def update(self):
        self.order = self.ypos + 1000
        self.spriteTimer += Time.deltaTime
        if self.spriteTimer >= self.spriteDelay and self.spriteIndex < 11:
            self.spriteTimer = 0
            self.spriteIndex += 1

        self.sprite = self.spriteImages[self.spriteIndex]
        if self.spriteIndex >= 11:
            ObjectLists.listAllObjects.remove(self)
            del self
