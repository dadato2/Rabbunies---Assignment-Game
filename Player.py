from Object import *
from Bomb_Variants import *

idle_animation = makeSprite("assets/rabber_idle.png", 4).images
for i in range(0, 4):
    idle_animation[i] = pygame.transform.scale(idle_animation[i], (54, 78))

running_animation = makeSprite("assets/rabber_running.png", 6).images
for i in range(0, 6):
    running_animation[i] = pygame.transform.scale(running_animation[i], (54, 78))



class Player (Object):
    def __init__(self):

        Global.player = self

        self.Health = 3
        self.maxHealth = 5
        self.speed = 6

        # how many bombs does the player have, -1 = infinity
        self.bombInventory = [-1, 5, 3, 2, 1, 0]

        # sprite handlings
        self.anim_idle = idle_animation
        self.anim_run = running_animation
        self.animIndex = 0
        self.animDelay = random.randrange(16, 24) * 0.01
        self.animTimer = 0
        self.isFacingLeft = False
        self.invincible = 0
        self.invincibleTime = 2  # seconds
        self.newBomb = None

        self.sprite = self.anim_idle[self.animIndex]
        self.rect = self.sprite.get_rect()
        # self.Sound_tear_1 = Global.Sounds.player_tear_1

        #positional and movement
        self.ypos = 300
        self.xpos = 300
        self.order = self.ypos + self.rect.h
        self.decel = self.speed / 1.5
        self.accel = self.speed / 1.5
        self.xAcc = 0.0
        self.yAcc = 0.0
        self.tempxAcc = 0.0
        self.tempyAcc = 0.0
        self.running = False
        # can only thow one bomb at a time
        self.bombPresent = False

        self.pKey = None

    def update(self):
        self.pKey = pygame.key.get_pressed()
        # walking:
        self.walk()
        # shooting:
        self.shooting()
        # set sprite
        self.animate()

        # collisions
        if self.invincible <= 0:
            for explosion in ObjectLists.listOfExplosions:
                if self.rect.colliderect(explosion.rect) and explosion.spriteIndex < 2:
                    self.Health -= 1
                    self.invincible = self.invincibleTime


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
        if self.invincible > 0:
            self.invincible -= Time.deltaTime
            if math.sin(self.invincible*50) >= 0:
                self.sprite = self.sprite.copy()
                self.sprite.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)

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
        self.isCharging = pygame.mouse.get_pressed()[0]
        # checks which bomb is selected and spawns a bomb depending on that
        if not self.bombPresent and self.isCharging:
            if Global.SelectedBomb == 0 and (self.bombInventory[0] > 0 or self.bombInventory[0] < 0):
                self.newBomb = Dynamite(self)
            elif Global.SelectedBomb == 1 and (self.bombInventory[1] > 0 or self.bombInventory[1] < 0):
                self.newBomb = Round(self)
            elif Global.SelectedBomb == 2 and (self.bombInventory[2] > 0 or self.bombInventory[2] < 0):
                self.newBomb = Grenade(self)
            elif Global.SelectedBomb == 3 and (self.bombInventory[3] > 0 or self.bombInventory[3] < 0):
                self.newBomb = Carrot(self)
            elif Global.SelectedBomb == 4 and (self.bombInventory[4] > 0 or self.bombInventory[4] < 0):
                self.newBomb = Cube(self)
            elif Global.SelectedBomb == 5 and (self.bombInventory[5] > 0 or self.bombInventory[5] < 0):
                self.newBomb = Head(self)

            if self.bombInventory[Global.SelectedBomb] > 0:
                self.bombInventory[Global.SelectedBomb] -= 1
            self.bombPresent = True

