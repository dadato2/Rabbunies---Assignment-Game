from Object import *
class Crosshair (Object):
    def __init__(self):
        Global.Crosshair = self
        self.xpos, self.ypos = self.xy = (0, 0)
        self.order = self.ypos
        self.sprite = pygame.image.load("assets/crosshair.png")
        self._spriteOrigin = self.sprite
        self.spriteAngle = 0
        self.scaleTime = 2
        self.spriteScale = 0
        self.rect = self.sprite.get_rect()
        self.distFromPLayer = 0

    def update(self):
        self.distFromPLayer = math.sqrt((self.xpos-Global.player.xpos)*(self.xpos-Global.player.xpos) +
                                        (self.ypos-Global.player.ypos)*(self.ypos-Global.player.ypos))

        self.mKey = pygame.mouse.get_pressed()
        if self.mKey[0]:
            self.spriteAngle += 2
            if self.spriteScale < self.scaleTime:
                self.spriteScale += Time.deltaTime
        else:
            if self.spriteAngle > 0:
                self.spriteAngle -= 2
            if 175 < self.spriteAngle < 185:
                self.spriteAngle = 0
            if self.spriteScale > 0:
                self.spriteScale -= Time.deltaTime*20
            if self.spriteScale < 0:
                self.spriteScale = 0

        self.spriteAngle %= 360
        self.sprite = pygame.transform.rotate(self._spriteOrigin, self.spriteAngle)
        self.spriteScaleX = self.spriteScaleY = int(self.spriteScale*25 + 50)
        self.sprite = pygame.transform.scale(self.sprite, (self.spriteScaleX, self.spriteScaleY))

        self.order = Constants.scr_height
        self.rect = self.sprite.get_rect()

        self.xpos, self.ypos = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

    def draw(self, screen):
        self.xy = (pygame.mouse.get_pos()[0] - self.rect.center[0], pygame.mouse.get_pos()[1] - self.rect.center[1])
        screen.blit(self.sprite, self.xy)
