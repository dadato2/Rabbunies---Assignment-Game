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


enemyX, enemyY = 27, 39
enemyImages = makeSprite("assets/enemyImages.png", 3).images
for imageIndex in range(0, len(enemyImages)):
    enemyImages[imageIndex] = pygame.transform.scale(enemyImages[imageIndex], (enemyX, enemyY))


class UI_Enemies(UI_Object):
    def __init__(self):
        self.xpos = 10
        self.ypos = Constants.scr_height-50
        self.font = pygame.font.Font('assets/arcade.ttf', 40)
        self.message = "Enemies   left"
        self.images = enemyImages
        self.layer = 1

    def draw(self, screen):
        screen.blit(self.font.render(self.message, False, (0, 0, 0)), (self.xpos, self.ypos))
        enemyIterator = 0
        for enemy in ObjectLists.listOfEnemies:
            screen.blit(self.images[enemy.selfType], (self.xpos + 260 + (enemyX + 15)* enemyIterator, self.ypos))
            enemyIterator += 1


