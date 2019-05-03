from Object import *
from Bomb import Bomb

# tmpisaacHead = makeSprite("assets/isaacHead.png", 8)
# isaacHead = tmpisaacHead.images
# tmpisaacBody = makeSprite("assets/isaacBody.png", 30)
# isaacBody = tmpisaacBody.images
playerSprite = pygame.image.load("assets/rabber.png")
newBomb = None

class Player (Object):
    def __init__(self):

        Global.player = self
        '''
        self.spriteIndexHead = 0
        self.spriteHead = isaacHead[self.spriteIndexHead]
        self.spriteIndexBody = 0
        self.spriteIndexAddTen = 0
        self.spriteBody = isaacBody[self.spriteIndexBody]
        self.spriteIndexBodyDelay = 0
        '''
        self.height = 66
        self.sprite = playerSprite
        # self.rect = self.spriteHead.get_rect()
        # self.Sound_tear_1 = Global.Sounds.player_tear_1

        self.ypos = 300
        self.xpos = 300

        self.squareSize = 66
        self.rect = self.sprite.get_rect()
        self.xy = (self.xpos - self.rect.center[0] + Constants.scr_shake_offset_x,
                   self.ypos - self.rect.center[1] + Constants.scr_shake_offset_y)
        self.order = self.ypos + self.squareSize
        self.speed = 6
        self.decel = self.speed / 1.5
        self.accel = self.speed / 1.5
        self.xAcc = 0.0
        self.yAcc = 0.0
        self.tempxAcc = 0.0
        self.tempyAcc = 0.0

        self.strength = 0
        self.maxStrength = 100

        self.bombDelay = 2
        self.bombDelayCounter = 0

        self.accuracyOffset = 5

        self.bombPresent = False

        self.isShooting = False
        self.pKey = pygame.key.get_pressed()

    def update(self):
        self.pKey = pygame.key.get_pressed()
        # walking:
        self.walk()
        # shooting:
        self.shooting()
        # set sprite
        # self.animateBody()


    def animateBody(self):
        if self.spriteIndexBodyDelay > 0:
            self.spriteIndexBodyDelay -= Time.deltaTime

        if self.spriteIndexBodyDelay <= 0:
            if not self.yAcc < 0:
                self.spriteIndexBody = (self.spriteIndexBody+1) % 10
            else:
                if self.spriteIndexBody > 0:
                    self.spriteIndexBody -= 1
                else:
                    self.spriteIndexBody = 10
        if self.spriteIndexBody > 10:
            self.spriteIndexBody = 10
        if -0.05 < self.tempxAcc <= 0.05 and -0.05 < self.tempyAcc <= 0.05:
            self.spriteIndexAddTen = 0
            self.spriteIndexBody = 0

        if math.fabs(self.tempxAcc) > math.fabs(self.tempyAcc):
            if self.tempxAcc < 0:
                self.spriteIndexAddTen = 20
                if self.spriteIndexBodyDelay <= 0:
                    self.spriteIndexBodyDelay = 0.1-(math.fabs(self.tempxAcc) / self.accel)/100
            if self.tempxAcc > 0:
                self.spriteIndexAddTen = 10
                if self.spriteIndexBodyDelay <= 0:
                    self.spriteIndexBodyDelay = 0.1-(math.fabs(self.tempxAcc) / self.accel)/100
        else:
            self.spriteIndexAddTen = 0
            if self.spriteIndexBodyDelay <= 0:
                self.spriteIndexBodyDelay = 0.1-(math.fabs(self.tempyAcc) / self.accel)/100

        if self.spriteIndexBody > 10:
            self.spriteIndexBody = 10
        if self.spriteIndexBody < 0:
            self.spriteIndexBody = 0

    def walk(self):    # temporary xAcc and yAcc act as acceleration (will add a delay in future)

        if self.pKey[K_d]:  # right
            if self.xAcc < 0:
                self.xAcc = 0
            if self.xAcc < self.speed:
                self.xAcc += self.accel/10
            if self.xpos > Constants.scr_width - self.rect.w:
                self.xAcc = -0.01

        if self.pKey[K_a]:  # left
            if self.xAcc > 0:
                self.xAcc = 0
            if self.xAcc > -self.speed:
                self.xAcc -= self.accel/10
            if self.xpos < 40:
                self.xAcc = 0.1

        if self.pKey[K_w]:  # up
            if self.yAcc > 0:
                self.yAcc = 0
            if self.yAcc > -self.speed:
                self.yAcc -= self.accel/10
            if self.ypos < 40:
                self.yAcc = 0.1

        if self.pKey[K_s]:  # down
            if self.yAcc < 0:
                self.yAcc = 0
            if self.yAcc < self.speed:
                self.yAcc += self.accel/10
            if self.ypos > Constants.scr_height - self.rect.h:
                self.yAcc = +0.1

        if not self.pKey[K_a] and not self.pKey[K_d]:   # manage deceleration for horizontal input
            for i in range(0, int(self.decel)):
                if self.xAcc > 0:
                    self.xAcc -= 0.1
                elif self.xAcc < 0:
                    self.xAcc += 0.1
            if -0.1 <= self.xAcc <= 0.1:
                self.xAcc = 0

        if not self.pKey[K_w] and not self.pKey[K_s]:    # manage deceleration for vertical input
            for i in range(0, int(self.decel)):
                if self.yAcc > 0:
                    self.yAcc -= 0.1
                elif self.yAcc < 0:
                    self.yAcc += 0.1
            if -0.1 <= self.yAcc <= 0.1:
                self.yAcc = 0

        if self.yAcc != 0 and self.xAcc != 0:
            self.tempyAcc = self.yAcc * 0.7071   # normalize diagonal movement
            self.tempxAcc = self.xAcc * 0.7071
        else:
            self.tempxAcc = self.xAcc   # if not diagonal set temp values to acceleration
            self.tempyAcc = self.yAcc   # the temp values are here only to normalize the diagonal movement btw

        self.xpos += int(self.tempxAcc)
        self.ypos += int(self.tempyAcc)

        # reset direction animation:


    def shooting(self):
        global newBomb
        self.isCharging = pygame.mouse.get_pressed()[0]

        if not self.bombPresent and self.isCharging:
            newBomb = Bomb()
            self.bombPresent = True

        if self.bombDelayCounter <= self.bombDelay and self.isCharging and self.bombPresent:    # manage delay between bombs, if you shoot a bomb, the counter resets and regains value over time
            self.bombDelayCounter += Time.deltaTime

        if not self.isCharging and self.bombDelayCounter > 0 and self.bombPresent:
            if newBomb != None:
                newBomb
            self.bombDelayCounter = 0


    def shootBomb(self):
        pass
        # new_bomb = Bomb(direction, self)


"""
    def draw(self, screen):
        self.order = self.ypos + self.squareSize
        self.xy = (self.xpos - self.rect.center[0] + Constants.scr_shake_offset_x,
                   self.ypos -self.rect.center[1] + Constants.scr_shake_offset_y)
        screen.blit(self.sprite, self.xy)
"""
