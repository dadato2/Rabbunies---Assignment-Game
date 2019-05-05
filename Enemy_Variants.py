from Enemy import *

idle_animation_bun1 = makeSprite("assets/bun1_idle.png", 4).images
for i in range(0, 4):
    idle_animation_bun1[i] = pygame.transform.scale(idle_animation_bun1[i], (54, 78))

running_animation_bun1 = makeSprite("assets/bun1_running.png", 6).images
for i in range(0, 6):
    running_animation_bun1[i] = pygame.transform.scale(running_animation_bun1[i], (54, 78))

idle_animation_bun2 = makeSprite("assets/bun2_idle.png", 4).images
for i in range(0, 4):
    idle_animation_bun2[i] = pygame.transform.scale(idle_animation_bun2[i], (54, 78))

running_animation_bun2 = makeSprite("assets/bun2_running.png", 6).images
for i in range(0, 6):
    running_animation_bun2[i] = pygame.transform.scale(running_animation_bun2[i], (54, 78))

idle_animation_bun3 = makeSprite("assets/bun3_idle.png", 4).images
for i in range(0, 4):
    idle_animation_bun3[i] = pygame.transform.scale(idle_animation_bun3[i], (54, 78))

running_animation_bun3 = makeSprite("assets/bun3_running.png", 6).images
for i in range(0, 6):
    running_animation_bun3[i] = pygame.transform.scale(running_animation_bun3[i], (54, 78))


class Bun1(Enemy):
    def __init__(self):
        super().__init__()
        self.Health = 2
        self.speed = 1
        self.accuracyOffset = 5
        self.bomb_type = "dynamite"
        self.bombDelayAdderMin, self.bombDelayAdderMax = 0, 3

        self.anim_idle = idle_animation_bun1
        self.anim_run = running_animation_bun1
        self.sprite = self.anim_idle[0]
        self.rect = self.sprite.get_rect()


class Bun2(Enemy):
    def __init__(self):
        super().__init__()
        self.Health = 2
        self.speed = 2
        self.accuracyOffset = 2
        self.bomb_type = "dynamite"
        self.bombDelayAdderMin, self.bombDelayAdderMax = -1, 2

        self.anim_idle = idle_animation_bun2
        self.anim_run = running_animation_bun2
        self.sprite = self.anim_idle[0]
        self.rect = self.sprite.get_rect()


class Bun3(Enemy):
    def __init__(self):
        super().__init__()
        self.Health = 3
        self.speed = 3
        self.accuracyOffset = 0
        self.bomb_type = "round"
        self.bombDelayAdderMin, self.bombDelayAdderMax = -1, 1

        self.anim_idle = idle_animation_bun3
        self.anim_run = running_animation_bun3
        self.sprite = self.anim_idle[0]
        self.rect = self.sprite.get_rect()
