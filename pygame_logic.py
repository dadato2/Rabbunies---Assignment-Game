# pygame_functions

# Documentation at www.github.com/stevepaget/pygame_functions
# Report bugs at https://github.com/StevePaget/Pygame_Functions/issues


import pygame, math, sys, os

class newSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        img = pygame.image.load(filename)
        self.originalWidth = img.get_width() // frames
        self.originalHeight = img.get_height()
        frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
        x = 0
        for frameNo in range(frames):
            frameSurf = pygame.Surface((self.originalWidth, self.originalHeight), pygame.SRCALPHA, 32)
            frameSurf.blit(img, (x, 0))
            self.images.append(frameSurf.copy())
            x -= self.originalWidth
        self.image = pygame.Surface.copy(self.images[0])

        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1

def loadImage(fileName, useColorKey=False):
    if os.path.isfile(fileName):
        image = pygame.image.load(fileName)
        # image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception("Error loading image: " + fileName + " - Check filename and path?")

def makeSprite(filename, frames=1):
    thisSprite = newSprite(filename, frames)
    return thisSprite


def addSpriteImage(sprite, image):
    sprite.addImage(image)


def changeSpriteImage(sprite, index):
    sprite.changeImage(index)


def nextSpriteImage(sprite):
    sprite.currentImage += 1
    if sprite.currentImage > len(sprite.images) - 1:
        sprite.currentImage = 0
    sprite.changeImage(sprite.currentImage)
