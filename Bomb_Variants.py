from Bomb import *

cubeSprite = makeSprite("assets/3dCube.png", 48).images
carrotSprite = pygame.image.load("assets/carrot.png")
bombSprite = pygame.image.load("assets/bomb.png")
grenadeSprite =pygame.image.load("assets/grenade.png")
dynamiteSprite = None
headSprite = pygame.image.load("assets/head.png")


class Dynamite(Bomb):
    def __init__(self):
        super().__init__()
        self.explosionScale = 200
        self.speed = 4

        self.spriteOrigin = carrotSprite
        self.scaledSpite = self.spriteOrigin
        self.sprite = self.spriteOrigin

    def update(self):
        super().update()


class Round(Bomb):
    def __init__(self):
        super().__init__()
        self.explosionScale = 250
        self.speed = 5

        self.spriteOrigin = bombSprite
        self.scaledSpite = self.spriteOrigin
        self.sprite = self.spriteOrigin

    def update(self):
        super().update()

class Grenade(Bomb):
    def __init__(self):
        super().__init__()
        self.explosionScale = 300
        self.speed = 6

        self.spriteOrigin = grenadeSprite
        self.scaledSpite = self.spriteOrigin
        self.sprite = self.spriteOrigin

    def update(self):
        super().update()


class Carrot(Bomb):
    def __init__(self):
        super().__init__()
        self.explosionScale = 350
        self.speed = 6

        self.spriteOrigin = carrotSprite
        self.scaledSpite = self.spriteOrigin
        self.sprite = self.spriteOrigin

    def update(self):
        super().update()


class Cube(Bomb):
    def __init__(self):
        super().__init__()
        self.explosionScale = 400
        self.speed = 7
        self.spriteImages = cubeSprite
        self.spriteIndex = 0
        self.spriteIndexCounter = 0
        self.spriteIndexDelay = 0.1

    def animate(self):
        self.spriteIndexCounter += Time.deltaTime
        if self.spriteIndexCounter >= self.spriteIndexDelay:
            self.spriteIndexDelay = 0
            self.spriteIndex += 1
            self.spriteIndex %= 48

    def update(self):
        self.animate()
        super().update()
        self.sprite = self.spriteImages[self.spriteIndex]


class Head(Bomb):
    def __init__(self):
        super().__init__()
        self.explosionScale = 500
        self.speed = 8

        self.spriteOrigin = headSprite
        self.scaledSpite = self.spriteOrigin
        self.sprite = self.spriteOrigin

    def update(self):
        super().update()

