from enum import Enum
import math, pygame


class globalMath:
    def __init__(self):
        self.temp = 0

    def Angle_noobj(self, originObject, x, y):
        return math.atan2((originObject.ypos - y),
                          (x - originObject.xpos)) + math.pi / 2

    def Angle(self, originObject, targetObject):
        return math.atan2((originObject.ypos - targetObject.ypos),
                          (targetObject.xpos - originObject.xpos)) + math.pi / 2

    def AnglePlayer(self, origin):
        return math.atan2((origin.ypos - Global.player.ypos),
                          (Global.player.xpos - origin.xpos)) + math.pi/2

    def DistFromPlayer(self, origin):
        return math.sqrt((origin.xpos-Global.player.xpos)*(origin.xpos-Global.player.xpos) +
                                        (origin.ypos-Global.player.ypos)*(origin.ypos-Global.player.ypos))

    def Dist(self, origin, target):
        return math.sqrt((origin.xpos-target.xpos)*(origin.xpos-target.xpos) +
                                        (origin.ypos-target.ypos)*(origin.ypos-target.ypos))

    def Dist_noObj(self, origin, targetX, targetY):
        return math.sqrt((origin.xpos-targetX)*(origin.xpos-targetX) +
                                        (origin.ypos-targetY)*(origin.ypos-targetY))



GlobalMath = globalMath()

class Global:
    player = None
    Sounds = None
    Crosshair = None
    scr = None
    wave = 0
    score = 0
    SelectedBomb = 0
    collected_bombs = [0, 0, 0, 0, 0]
    Debug = False

class Constants:
    scr_width = 1080
    scr_height = 720

    scr_shake_offset_x = 0
    scr_shake_offset_y = 0

    fps = 60
    caption = "Rabbunnies: The element of explode!"
    iconImage = "icon.png"

    debugMessage = ""

    playerWidth = 56
    playerHeight = 66

    enemycount = 0

class ObjectLists:
    listAllObjects = []
    listOfBombs = []
    listOfExplosions = []
    listOfEnemies = []
    listPickups = []
    listUI = []

class Time:
    deltaTime = 0.0

class Colors:
    black = 0, 0, 0
    white = 255, 255, 255
    red = 255, 0, 0
    yellow = 255, 255, 0
    green = 0, 255, 0
    cyan = 0, 255, 255
    blue = 0, 0, 255
    water = 90, 240, 255
    magenta = 255, 0, 255
    gray_very_light = 200, 200, 200
    gray_light = 175, 175, 175
    gray_dark = 75, 75, 75
    gray_very_dark = 50, 50, 50
    pleasant_red = 223, 117, 153
    pleasant_blue = 114, 214, 201
    pleasant_white = 255, 252, 241

class directions(Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3

'''class sounds:
    def __init__(self):
        self.player_tear_1 = pygame.mixer.Sound("assets/sfx/tear_fire_2.wav")
        self.tear_destroy = pygame.mixer.Sound("assets/sfx/tear_fire_1.wav")
        self.insect_swarm = pygame.mixer.Sound("assets/sfx/insect_swarm.wav")
'''
