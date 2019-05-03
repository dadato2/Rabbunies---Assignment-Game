# from Object import *
from ExtClasses import *
import random

class ScreenController():
    def __init__(self):
        self.timer = 0
        self.order = 0
        self.shakeDelay = 0.03
        self.timerOrigin = 0
        self.resolveTime = 0
        self.minusplusus = random.randint(0,1)
        self.minplus = 1
        self.shakeAmmount = 0
        self.shakeAmmountResolver =0

    def shakeScreen(self, ammount, resolveTime):
        self.shakeAmmount = ammount
        self.shakeAmmountResolver = ammount
        self.timerOrigin = resolveTime
        self.resolveTime = resolveTime

    def update(self):
        if self.timerOrigin > 0:
            self.timerOrigin -= Time.deltaTime
            self.timer += Time.deltaTime
            if self.timer >= self.shakeDelay:
                self.timer = 0
                if self.minusplusus == 0:
                    self.minplus = -1
                else:
                    self.minplus = 1
                if self.shakeAmmount > 1:
                    Constants.scr_shake_offset_x = random.randrange(int(-self.shakeAmmount), int(self.shakeAmmount))
                    Constants.scr_shake_offset_y = random.randrange(int(-self.shakeAmmount), int(self.shakeAmmount))
                self.shakeAmmount = (self.shakeAmmountResolver * float(self.timerOrigin/self.resolveTime)*100)/100


