from Object import *

bombSprites = makeSprite("assets/bombs.png", 6).images
eggSprites = makeSprite("assets/egg1.png", 4).images


class Pickup(Object):
    def __init__(self, objectSource):
        super().__init__()
        ObjectLists.listAllObjects.append(self)
        ObjectLists.listPickups.append(self)
        self.xpos = objectSource.xpos
        self.ypos = objectSource.ypos
        self.order = self.ypos
        self.typelist = ("health", "dynamite", "round", "grenade", "carrot", "cube", "head")
        if random.getrandbits(1):
            self.type = self.typelist[0]
            self.sprite = eggSprites[random.randrange(0, len(eggSprites))]
            self.sprite = pygame.transform.scale(self.sprite, (32, 32))
        else:
            self.chance = random.randrange(1, len(bombSprites))
            self.type = self.typelist[self.chance + 1]
            self.sprite = bombSprites[self.chance]
        self.rect = pygame.Rect(self.xpos - self.sprite.get_rect().w / 2, self.ypos - self.sprite.get_rect().h / 2,
                                self.sprite.get_rect().w, self.sprite.get_rect().h)

