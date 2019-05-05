from Object import *
from Bomb_Variants import Dynamite, Round

class Enemy(Object):
    def __init__(self):
        ObjectLists.listAllObjects.append(self)
        ObjectLists.listOfEnemies.append(self)
        # values to be changed by child class
        self.Health = 3
        self.speed = 6
        self.accuracyOffset = 5
        self.bomb_type = "dynamite"
        self.bombDelayAdderMin, self.bombDelayAdderMax = 0, 0

        # sprite handlings
        self.anim_idle = None
        self.anim_run = None
        self.animIndex = random.randrange(0,4)
        self.animDelay = random.randrange(16, 24) * 0.01
        self.animTimer = 0
        self.isFacingLeft = False
        self.running = False
        self.newBomb = None
        # draw
        self.sprite = None
        self.rect = None
        self.ypos = random.randrange(30, Constants.scr_height-30)
        self.xpos = random.randrange(30, Constants.scr_width-30)
        self.order = self.ypos
        self.invincible = 0
        self.invincibleTime = 2  # seconds
        # movement and position
        self.targetDest = (random.randrange(0, Constants.scr_width),
                           random.randrange(0, Constants.scr_height))
        self.decel = self.speed / 1.5
        self.accel = self.speed / 1.5
        self.xAcc = 0.0
        self.yAcc = 0.0
        self.direction = None
        self.bombPresent = False
        self.pKey = pygame.key.get_pressed()
        self.distFromPlayer = 100
        self.distFromTarget = 0
        self.waitThere = 0
        # bomb throwing
        self.bombDelay = 5
        self.bombDelayCounter = random.randrange(300, 500) * 0.01

    def update(self):
        if self.Health <= 0:
            ObjectLists.listOfEnemies.remove(self)
            ObjectLists.listAllObjects.remove(self)
            return

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

        if self.waitThere <= 0:
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
            if math.sin(self.invincible*50)>=0:
                self.sprite = self.sprite.copy()
                self.sprite.fill((0,0,0), special_flags=pygame.BLEND_ADD)
            else:
                self.sprite = self.sprite.copy()
                self.sprite.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)

    def walk(self):
        self.distFromPlayer = GlobalMath.DistFromPlayer(self)
        self.distFromTarget = GlobalMath.Dist_noObj(self, self.targetDest[0], self.targetDest[1])
        self.direction = GlobalMath.Angle_noobj(self, self.targetDest[0], self.targetDest[1])
        self.xAcc = math.sin(self.direction) * self.speed
        self.yAcc = math.cos(self.direction) * self.speed

        # self.enemyCollision()
        if self.distFromTarget > 1 and self.waitThere <= 0:
            self.xpos = round(self.xpos +self.xAcc)
            self.ypos = round(self.ypos +self.yAcc)
        elif self.waitThere <= 0:
            self.waitThere = random.randrange(0, 2)
            self.targetDest =(random.randrange(30, Constants.scr_width-30-self.rect.w),
                           random.randrange(30, Constants.scr_height-30-self.rect.w))
        if self.waitThere > 0:
            self.waitThere -= Time.deltaTime
            self.yAcc = 0
            self.xAcc = 0


    def enemyCollision(self):
        for enem in ObjectLists.listOfEnemies:
            if self.rect.colliderect(enem.rect):
                if enem.ypos <= self.ypos <= enem.ypos + enem.rect.w/2 and enem.xpos < self.xpos <= enem.xpos + enem.rect.w:
                    self.ypos += self.speed
                    enem.ypos -= enem.speed
                elif enem.ypos + enem.rect.w/2 > self.ypos >= enem.rect.w and enem.xpos < self.xpos <= enem.xpos + enem.rect.w:
                    self.ypos -= self.speed
                    enem.ypos += enem.speed
                if enem.xpos <= self.xpos <= enem.xpos + enem.rect.h/2 and enem.ypos < self.ypos <= enem.ypos + enem.rect.h:
                    self.xpos += self.speed
                    enem.xpos -= enem.speed
                elif enem.xpos + enem.rect.h/2 > self.xpos >= enem.rect.h and enem.ypos < self.ypos <= enem.ypos + enem.rect.h:
                    self.xpos -= self.speed
                    enem.xpos += enem.speed

    def shooting(self):
        self.bombDelayCounter -= Time.deltaTime
        if self.bombDelayCounter <= 0:
            self.bombDelayCounter = self.bombDelay + random.randrange(self.bombDelayAdderMin, self.bombDelayAdderMax)
            if self.bomb_type == "dynamite":
                self.newBomb = Dynamite(self)
            else:
                self.newBomb = Round(self)
            self.newBomb.thrown = True
            self.newBomb.direction = GlobalMath.AnglePlayer(self) # + random.randrange(-self.accuracyOffset, self.accuracyOffset)
            self.newBomb.fuseOriginal = self.newBomb.fuse = self.distFromPlayer / (50*self.newBomb.speed) #  random.randrange(1, self.accuracyOffset) * 0.5
