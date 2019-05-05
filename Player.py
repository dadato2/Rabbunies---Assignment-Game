from Object import *
from Bomb_Variants import *

idle_animation = makeSprite("assets/rabber_idle.png", 4).images
for i in range(0, 4):
    idle_animation[i] = pygame.transform.scale(idle_animation[i], (54, 78))

running_animation = makeSprite("assets/rabber_running.png", 6).images
for i in range(0, 6):
    running_animation[i] = pygame.transform.scale(running_animation[i], (54, 78))

newBomb = None

class Player (Object):
    def __init__(self):

        Global.player = self
        # sprite handlings
        self.anim_idle = idle_animation
        self.anim_run = running_animation
        self.animIndex = 0
        self.animDelay = 0.2
        self.animTimer = 0
        self.isFacingLeft = False

        self.sprite = self.anim_idle[self.animIndex]
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
        self.running = False
        self.tempxAcc = 0.0
        self.tempyAcc = 0.0

        self.strength = 0
        self.maxStrength = 100

        self.bombDelay = 2
        self.bombDelayCounter = 0

        self.accuracyOffset = 5

        self.bombPresent = False

        self.pKey = pygame.key.get_pressed()

    def update(self):
        self.pKey = pygame.key.get_pressed()
        # walking:
        self.walk()
        # shooting:
        self.shooting()
        # set sprite
        self.animate()

    def animate(self):
        if self.xAcc < 0:
            self.isFacingLeft = False
        else:
            self.isFacingLeft = True

        if self.yAcc != 0 or self.xAcc != 0:
            self.running = True
            self.animDelay = 0.1
        else:
            self.running = False
            self.animDelay = 0.2

        if not self.running:
            self.animIndex %= 4
            self.animTimer += Time.deltaTime
            if self.animTimer >= self.animDelay:
                self.animTimer = 0
                self.animIndex = (self.animIndex+1) % 4
            self.sprite = self.anim_idle[self.animIndex]
        else:
            self.animIndex %= 6
            self.animTimer += Time.deltaTime
            if self.animTimer >= self.animDelay:
                self.animTimer = 0
                self.animIndex = (self.animIndex + 1) % 6
            if self.isFacingLeft:
                self.sprite = self.anim_run[self.animIndex]
            else:
                self.sprite = pygame.transform.flip(self.anim_run[self.animIndex], True, False)

    def walk(self):    # pressing movement keys WASD increases/decreases acceleration

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
            i = random.randrange(0, 6)
            if i == 0:
                newBomb = Dynamite(self)
            elif i == 1:
                newBomb = Round(self)
            elif i == 2:
                newBomb = Grenade(self)
            elif i == 3:
                newBomb = Carrot(self)
            elif i == 4:
                newBomb = Cube(self)
            else:
                newBomb = Head(self)
            self.bombPresent = True

        if self.bombDelayCounter <= self.bombDelay and self.isCharging and self.bombPresent:    # manage delay between bombs, if you shoot a bomb, the counter resets and regains value over time
            self.bombDelayCounter += Time.deltaTime

        if not self.isCharging and self.bombDelayCounter > 0 and self.bombPresent:
            if newBomb != None:
                newBomb
            self.bombDelayCounter = 0
