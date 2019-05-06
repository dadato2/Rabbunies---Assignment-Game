from UI_Object import *

egg_x, egg_y = 64, 64

egg_1 = pygame.image.load("assets/egg1.png")
egg_1 = pygame.transform.scale(egg_1, (egg_x, egg_y))

class UI_Health(UI_Object):
    def __init__(self):
        self.xpos = 10
        self.ypos = 10
        self.layer = 0
        self.image = egg_1.convert()

    def draw(self, screen):
        for eggs in range(0, Global.player.Health):
            screen.blit(self.image, (self.xpos + egg_x * eggs, self.ypos))