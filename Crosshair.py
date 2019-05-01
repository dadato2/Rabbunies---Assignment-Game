from Object import *
class Crosshair (Object):
    def __init__(self):

        self.x, self.y = self.xy = (0,0)
        self.order = self.y
        self.sprite = pygame.image.load("assets/crosshair.png")
        self._spriteOrigin = self.sprite
        self.spriteAngle = 0
        self.spriteScale = 0
        self.rect = self.sprite.get_rect()



    def update(self):
        self.mKey = pygame.mouse.get_pressed()

        if self.mKey[0]:
            self.spriteAngle += 2
            if self.spriteScale < 50:
                self.spriteScale += 2
        else:
            if self.spriteAngle > 0:
                self.spriteAngle -= 2
            if 175 < self.spriteAngle < 185:
                self.spriteAngle = 0
            if self.spriteScale > 0:
                self.spriteScale -= 2


        self.spriteAngle %= 360
        self.sprite = pygame.transform.rotate(self._spriteOrigin, self.spriteAngle)
        self.spriteScaleX = self.spriteScaleY = int(self.spriteScale + 50)
        self.sprite = pygame.transform.scale(self.sprite, (self.spriteScaleX, self.spriteScaleY))

    def draw(self, screen):
        self.order = screen.get_height()
        self.rect = self.sprite.get_rect()
        self.xy = (pygame.mouse.get_pos()[0] - self.rect.center[0], pygame.mouse.get_pos()[1] - self.rect.center[1])
        screen.blit(self.sprite, self.xy)
