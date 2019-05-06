from enum import Enum
import math, pygame


class globalMath:   # methods that are used often in different classes
    def __init__(self):
        self.temp = 0

    def Angle_noobj(self, originObject, x, y):  # get angle between object and (x, y) coordinates
        return math.atan2((originObject.ypos - y),
                          (x - originObject.xpos)) + math.pi / 2

    def Angle(self, originObject, targetObject):    # get angle between object and other object
        return math.atan2((originObject.ypos - targetObject.ypos),
                          (targetObject.xpos - originObject.xpos)) + math.pi / 2

    def AnglePlayer(self, origin):  # get angle between object and player
        return math.atan2((origin.ypos - Global.player.ypos),
                          (Global.player.xpos - origin.xpos)) + math.pi/2

    def DistFromPlayer(self, origin):   # get distance from player, in pixels
        return math.sqrt((origin.xpos-Global.player.xpos)*(origin.xpos-Global.player.xpos) +
                                        (origin.ypos-Global.player.ypos)*(origin.ypos-Global.player.ypos))

    def Dist(self, origin, target):     # get distance from object to other object
        return math.sqrt((origin.xpos-target.xpos)*(origin.xpos-target.xpos) +
                                        (origin.ypos-target.ypos)*(origin.ypos-target.ypos))

    def Dist_noObj(self, origin, targetX, targetY):     # get distance from object to (x, y) coordinates
        return math.sqrt((origin.xpos-targetX)*(origin.xpos-targetX) +
                                        (origin.ypos-targetY)*(origin.ypos-targetY))


GlobalMath = globalMath() # creates object of global math


class Global:       # global variables used in different cases
    player = None   # player object
    Sounds = None    # not used at the moment
    Crosshair = None       #
    scr = None      # screen surface
    wave = 0    # which wave of enemies it is
    score = 0   # score
    SelectedBomb = 0    # id number of bomb selected
    collected_bombs = [0, 0, 0, 0, 0]   # used to keep track of wether a bomb has been collected before
    Debug = False   # debug mode, for debugging purposes


class Constants:   # constant values (even though some are changed)
    scr_width = 1080
    scr_height = 720

    scr_shake_offset_x = 0  # by how much to offset all sprites, handled in exploding
    scr_shake_offset_y = 0

    fps = 60
    caption = "Rabbunnies: The element of explode!"
    iconImage = "icon.png"

    debugMessage = ""  # used in Debug.Log()


class ObjectLists:      # every object list used
    listAllObjects = []
    listOfBombs = []
    listOfExplosions = []
    listOfEnemies = []
    listPickups = []
    listUI = []


class Time:   # this way I can type time.deltaTime to get time between each frame
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

'''class sounds:
    def __init__(self):
        self.player_tear_1 = pygame.mixer.Sound("assets/sfx/tear_fire_2.wav")
        self.tear_destroy = pygame.mixer.Sound("assets/sfx/tear_fire_1.wav")
        self.insect_swarm = pygame.mixer.Sound("assets/sfx/insect_swarm.wav")
'''
