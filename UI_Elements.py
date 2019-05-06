from UI_Object import *
import random

egg_x, egg_y = 64, 64

egg_1 = makeSprite("assets/egg1.png", 4).images
for times in range(0, len(egg_1)):
    egg_1[times] = pygame.transform.scale(egg_1[times], (egg_x, egg_y))


class UI_Health(UI_Object):
    def __init__(self):
        self.xpos = 10
        self.ypos = 10
        self.layer = 0
        self.images = egg_1
        self.eggIndex = []
        for times in range(0, 10):
            self.eggIndex.append(random.randrange(0, len(self.images)))

    def draw(self, screen):
        for eggs in range(0, Global.player.Health):
            screen.blit(self.images[self.eggIndex[eggs]], (self.xpos + egg_x * eggs, self.ypos))


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


bombX, bombY = 43, 43
bombImages = makeSprite("assets/bombs.png", 6).images
for imageIndex in range(0, len(bombImages)):
    bombImages[imageIndex] = pygame.transform.scale(bombImages[imageIndex], (bombX, bombY))


class UI_SelectedBomb(UI_Object):
    def __init__(self):
        self.xpos = Constants.scr_width - 100
        self.ypos = 10
        self.font = pygame.font.Font('assets/arcade.ttf', 40)
        self.message = "0"
        self.images = bombImages
        self.layer = 1

    def draw(self, screen):
        screen.blit(self.images[Global.SelectedBomb], (self.xpos, self.ypos))
        if Global.player.bombInventory[Global.SelectedBomb] <= -1:
            self.message = "oo"
        else:
            self.message = str(Global.player.bombInventory[Global.SelectedBomb])
        screen.blit(self.font.render(self.message, False, (0, 0, 0)), (self.xpos + bombX + 10, self.ypos))

