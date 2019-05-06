from Object import *
from Bomb_Variants import Dynamite, Round
from Pickup import Pickup

class Enemy(Object):
    def __init__(self):
        ObjectLists.listAllObjects.append(self) # appends itself to the global objects list
        ObjectLists.listOfEnemies.append(self)
        # values to be changed by child class
        self.Health = 3  # hitpoints
        self.speed = 6
        self.accuracyOffset = 5   # not used
        self.bomb_type = "dynamite"    # what type of bomb does the enemy throw
        self.bombDelayAdderMin, self.bombDelayAdderMax = 0, 0  # delay between throws, used to make enemies harder/easier
        self.selfType = 0   # which enemy it is (used for score)

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
        self.xpos = random.randrange(-300, Constants.scr_width +300)   # this code spawns the enemy off the screen
        if 0 < self.xpos < Constants.scr_width:
            if random.getrandbits:
                self.ypos = random.randrange(-300, -100)
            else:
                self.ypos = random.randrange(Constants.scr_height + 10, Constants.scr_height + 300)
        else:
            self.ypos = random.randrange(-300, Constants.scr_height + 300)

        self.order = self.ypos
        self.invincible = 0 # how long enemy is invincible after hit
        self.invincibleTime = 2  # seconds
        # movement and position
        self.targetDest = (random.randrange(0, Constants.scr_width),  # takes a point on the screen and moves toward it
                           random.randrange(0, Constants.scr_height))
        self.xAcc = 0.0  # used for
        self.yAcc = 0.0
        self.direction = None
        self.bombPresent = False
        self.pKey = pygame.key.get_pressed()
        self.distFromPlayer = 100
        self.distFromTarget = 0
        self.waitThere = 0 # time to wait at destination until getting another target destination
        # bomb throwing
        self.bombDelay = 5
        self.bombDelayCounter = random.randrange(500, 800) * 0.01

    def update(self):
        # Death
        if self.Health <= 0:
            Global.score += self.selfType+1
            ObjectLists.listOfEnemies.remove(self)
            ObjectLists.listAllObjects.remove(self)
            if random.randrange(0, 100) > 15:
                Pickup(self)
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
        # handles animation, if not moving, uses Idle sprites; if moving takes direction and
        # if needed flips the sprites
        # upon getting hit adds white tint to sprite that is flashing
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
        # walks to set destination (x, y). when it reaches it, waits a random between (0, 2) seconds
        # after that gets new destination and runs there
        self.distFromPlayer = GlobalMath.DistFromPlayer(self)
        self.distFromTarget = GlobalMath.Dist_noObj(self, self.targetDest[0], self.targetDest[1])
        self.direction = GlobalMath.Angle_noobj(self, self.targetDest[0], self.targetDest[1])
        self.xAcc = math.sin(self.direction) * self.speed
        self.yAcc = math.cos(self.direction) * self.speed

        # self.enemyCollision()
        if self.distFromTarget > 5 and self.waitThere <= 0:
            self.xpos = round(self.xpos +self.xAcc)
            self.ypos = round(self.ypos +self.yAcc)
        elif self.waitThere <= 0:
            self.waitThere = random.randrange(0, 200) * 0.01
            self.targetDest = (random.randrange(30, Constants.scr_width-30-self.rect.w),
                               random.randrange(30, Constants.scr_height-30-self.rect.w))
        if self.waitThere > 0:
            self.waitThere -= Time.deltaTime
            self.yAcc = 0
            self.xAcc = 0

    def shooting(self):
        # shoots a bomb at player at semi-random intervals
        self.bombDelayCounter -= Time.deltaTime
        if self.bombDelayCounter <= 0:
            self.bombDelayCounter = self.bombDelay + random.randrange(self.bombDelayAdderMin, self.bombDelayAdderMax)
            if self.bomb_type == "dynamite":
                self.newBomb = Dynamite(self)
            else:
                self.newBomb = Round(self)
            self.newBomb.thrown = True
            self.newBomb.direction = GlobalMath.AnglePlayer(self)
            self.newBomb.fuseOriginal = self.newBomb.fuse = self.distFromPlayer / (50*self.newBomb.speed)
