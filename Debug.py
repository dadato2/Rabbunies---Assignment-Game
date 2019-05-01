import pygame
from ExtClasses import Constants

class debug:

    def __init__(self):
        pygame.font.init()
        self.debugFont = pygame.font.SysFont('Comic Sans MS', 40)
        self.debugtextsurface = self.debugFont.render(Constants.debugMessage, False, (0, 0, 0))
        self.arg = ""
        self.prevarg = ""
    def Log(self, argument):
        try:
            self.arg = str(argument)
        except:
            print("Debug error in class debug!")
        if self.arg != self.prevarg:
            self.debugtextsurface = self.debugFont.render(self.arg, False, (0, 0, 0))
        self.prevarg = self.arg

