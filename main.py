import sys, operator
from ExtClasses import *
from Debug import *
from Crosshair import *
from Player import *
from Enemy_Variants import *
from Bomb import *
from UI_Elements import UI_Health, UI_Enemies, UI_SelectedBomb
from ScreenControl import ScreenController

pygame.init()
pygame.mixer.init()
time = pygame.time.Clock()
pygame.display.set_caption(Constants.caption)
screen = pygame.display.set_mode((Constants.scr_width, Constants.scr_height))
gameIcon = pygame.image.load(Constants.iconImage)
pygame.display.set_icon(gameIcon)
Debug = debug()
scr = ScreenController()
Global.scr = scr
# Global.Sounds = sounds()
gameLoop = True

font_arcade_40 = pygame.font.Font('assets/arcade.ttf', 40)
font_arcade_120 = pygame.font.Font('assets/arcade.ttf', 120)


def transition(color):
    size_of_Circle = 1
    while True:
        if size_of_Circle >= Constants.scr_width:
            break
        size_of_Circle *= 1.1
        time.tick(Constants.fps)
        pygame.draw.circle(screen, color, (int(Constants.scr_width / 2), int(Constants.scr_height / 2)),
                           int(size_of_Circle))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()


help_msg_1 = "Press   H   for   help!"
help_msg_2 = ""
while True:     # T I T L E   S C R E E N
    time.tick(Constants.fps)
    screen.fill(Colors.pleasant_red)
    screen.blit(font_arcade_120.render("Rabbunnies!", False, (255, 255, 255)), (160, 100))
    screen.blit(font_arcade_40.render("Press   Space   to   start!", False, (0, 0, 0)), (310, 400))
    screen.blit(font_arcade_40.render(help_msg_1, False, (0, 0, 0)), (310, 500))
    if not help_msg_2 == "":
        screen.blit(font_arcade_40.render(help_msg_2, False, (0, 0, 0)), (120, 550))

    if pygame.key.get_pressed()[K_SPACE]:
        transition(Colors.pleasant_blue)
        break
    if pygame.key.get_pressed()[K_h]:
        help_msg_1 = "WASD  move    MOUSE   aim"
        help_msg_2 = "HOLD   CLICK   TO   CHARGE   BOMB    RELEASE    TO    THROW"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()

# M A I N   L O O P   I N I T I A L I Z E
while gameLoop:
    # initialize and set main objects and UI objects
    player = Player()
    ObjectLists.listAllObjects.append(player)
    crosshair = Crosshair()
    ObjectLists.listAllObjects.append(crosshair)
    healthUI = UI_Health()
    ObjectLists.listUI.append(healthUI)
    enemyUI = UI_Enemies()
    ObjectLists.listUI.append(enemyUI)
    bombUI = UI_SelectedBomb()
    ObjectLists.listUI.append(bombUI)
    Global.SelectedBomb = 0
    Global.score = 0
    Global.wave = 1

    # now time and last time used to get time between each frame (smooth out animations, movements, etc.)
    nowTime = pygame.time.get_ticks()
    lastTime = nowTime
    # variable to pause enemy spawning between waves
    waitAMinute = 2
    # variable to pause switching between bombs
    bombSwitchDelay = 0.2
    waitForBombSwitch = bombSwitchDelay

    while True:                 # M A I N   L O O P
        nowTime = pygame.time.get_ticks()
        Time.deltaTime = (nowTime-lastTime) / 1000 % 1
        lastTime = nowTime
        time.tick(Constants.fps)
        pKey = pygame.key.get_pressed()
        if waitForBombSwitch < bombSwitchDelay:
            waitForBombSwitch += Time.deltaTime
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and waitForBombSwitch >= bombSwitchDelay:
                    Global.SelectedBomb = (Global.SelectedBomb - 1) % 6
                    while player.bombInventory[Global.SelectedBomb] == 0:
                        Global.SelectedBomb = (Global.SelectedBomb - 1) % 6
                    waitForBombSwitch = 0
                elif event.button == 5 and waitForBombSwitch >= bombSwitchDelay:
                    Global.SelectedBomb = (Global.SelectedBomb + 1) % 6
                    while player.bombInventory[Global.SelectedBomb] == 0:
                        Global.SelectedBomb = (Global.SelectedBomb + 1) % 6
                    waitForBombSwitch = 0

        pygame.display.update()

        if pKey[K_ESCAPE]:
            sys.exit()
        # if player dies transition to GAME OVER screen
        if player.Health <= 0:
            transition(Colors.black)
            break
        # sort objects based on their Y position
        ObjectLists.listAllObjects.sort(key=operator.attrgetter('order'))
        # sort UI objects based on their layer
        ObjectLists.listUI.sort(key=operator.attrgetter('layer'))
        screen.fill(Colors.pleasant_blue)
        scr.update()
        # update and draw all game objects
        for gameObject in ObjectLists.listAllObjects:
            gameObject.update()
            gameObject.draw(screen)
        # update and draw all UI objects
        for ui_object in ObjectLists.listUI:
            ui_object.update()
            ui_object.draw(screen)
        # control delay between waves
        if waitAMinute > 0 and len(ObjectLists.listOfEnemies) == 0:
            waitAMinute -= Time.deltaTime
        # spawn enemies depending on wave
        if len(ObjectLists.listOfEnemies) <= 0 and waitAMinute <= 0:
            waitAMinute = random.randrange(2, 4)
            Global.wave += 1
            for times in range(0, random.randrange(0, int(Global.wave/2)+1)):
                idd = random.randrange(Global.wave)
                if 0 <= idd < 3:
                    enemy = Bun1()
                elif 3 <= idd < 6:
                    enemy = Bun2()
                else:
                    enemy = Bun3()
        screen.blit(Debug.debugtextsurface, (10, 10))

    # reset all lists and variables
    ObjectLists.listAllObjects = []
    ObjectLists.listOfEnemies = []
    ObjectLists.listUI = []
    ObjectLists.listOfExplosions = []
    ObjectLists.listOfBombs = []
    Constants.scr_shake_offset_y = 0
    Constants.scr_shake_offset_x = 0
    scr.shakeAmmount = 0
    scr.shakeAmmountResolver = 0

    while True:     # GAME OVER SCREEN
        time.tick(Constants.fps)
        screen.fill(Colors.black)
        screen.blit(font_arcade_120.render("Game Over!", False, (255, 255, 255)), (250, 200))
        screen.blit(font_arcade_40.render("Press   Space   to   restart!", False, (255, 255, 255)), (310, 500))

        if pygame.key.get_pressed()[K_SPACE]:
            transition(Colors.pleasant_blue)
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()

