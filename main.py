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
pygame.mouse.set_visible(False)
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

font_arcade_26 = pygame.font.Font('assets/arcade.ttf', 26)
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


def showInfo(elem):
    infoRect_x, infoRect_y = Constants.scr_width * 1/6, Constants.scr_height * 1/6
    infoRect = pygame.Rect(infoRect_x, infoRect_y, Constants.scr_width * 5/6-infoRect_x,
                           Constants.scr_height * 5/6-infoRect_y)
    info_image_size = 96
    info_image = None
    info_images = None
    info_images_index = 0
    info_multiple_images = False
    info_msg_name = ""
    info_msg_1 = ""
    info_msg_2 = ""
    info_msg_3 = ""
    info_msg_4 = ""
    info_msg_goBack = "Press   Space   to   Continue"
    if elem == 0:
        info_image = pygame.image.load("assets/bomb.png")
        info_image = pygame.transform.scale(info_image, (info_image_size, info_image_size))
        info_msg_name = "Round   Bomb"
        info_msg_1 = "A   normal  round  bomb!"
        info_msg_2 = "The   Rabbits  have   watched   too   many"
        info_msg_3 = "Cartoons   in   their   youth   and  "
        info_msg_4 = " came   up   with   this!"
    elif elem == 1:
        info_image = pygame.image.load("assets/grenade.png")
        info_image = pygame.transform.scale(info_image, (info_image_size, info_image_size))
        info_msg_name = "Grenade"
        info_msg_1 = "Yes   rabbits   play   video   games"
        info_msg_2 = "That   is   how   they   came  up"
        info_msg_3 = "with   this   bomb!"
        info_msg_4 = "Quite   handy   if   you   ask   me!"
    elif elem == 2:
        info_image = pygame.image.load("assets/carrot.png")
        info_image = pygame.transform.scale(info_image, (info_image_size, info_image_size))
        info_msg_name = "Radioactive   Carrot"
        info_msg_1 = "Someone   left   this   carrot   in"
        info_msg_2 = "the   fridge   for   quite   a   long"
        info_msg_3 = "time!   Now   it   is  not   only"
        info_msg_4 = "stinky   but   also   explosive!"
    elif elem == 3:
        info_multiple_images = True
        info_images = makeSprite("assets/3dCube.png", 48).images
        for inin in range(0, len(info_images)):
            info_images[inin] = pygame.transform.scale(info_images[inin], (info_image_size, info_image_size))
        info_msg_name = "3D   Cube"
        info_msg_1 = "An   object   from   another   dimention!"
        info_msg_2 = "Rabbits   are   still   not   sure"
        info_msg_3 = "how   it   moves   on   its   own"
        info_msg_4 = "or   what   the   heck   it  is!"
    elif elem == 4:
        info_image = pygame.image.load("assets/head.png")
        info_image = pygame.transform.scale(info_image, (info_image_size, info_image_size))
        info_msg_name = "Head   Of  A   Fallen   Hero"
        info_msg_1 = "During   funerals   rabbits"
        info_msg_2 = "decapitate   their   fallen   brothers"
        info_msg_3 = "and   stuff   their   heads  with"
        info_msg_4 = "explosives!  Whoah!"
    while True:
        time.tick(Constants.fps)
        pygame.draw.rect(screen, Colors.pleasant_white, infoRect)
        pygame.draw.rect(screen, Colors.gray_very_dark, infoRect, 2)
        if info_multiple_images:
            screen.blit(info_images[info_images_index], (infoRect_x + 30, infoRect_y + 30))
            info_images_index = (info_images_index + 1) % 48
        else:
            screen.blit(info_image, (infoRect_x + 30, infoRect_y + 30))
        screen.blit(font_arcade_40.render(info_msg_name, False, (0, 0, 0)), (infoRect_x + 150, infoRect_y + 50))
        screen.blit(font_arcade_40.render(info_msg_1, False, (0, 0, 0)), (infoRect_x + 30, infoRect_y + 170))
        screen.blit(font_arcade_40.render(info_msg_2, False, (0, 0, 0)), (infoRect_x + 30, infoRect_y + 230))
        screen.blit(font_arcade_40.render(info_msg_3, False, (0, 0, 0)), (infoRect_x + 30, infoRect_y + 290))
        screen.blit(font_arcade_40.render(info_msg_4, False, (0, 0, 0)), (infoRect_x + 30, infoRect_y + 350))
        screen.blit(font_arcade_26.render(info_msg_goBack, False, (0, 0, 0)), (infoRect_x + 210, infoRect_y + 450))

        if pygame.key.get_pressed()[K_SPACE]:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()


help_msg_1 = "Press   H   for   help!"
help_msg_2 = ""
help_msg_3 = ""
while True:                                                                      # T I T L E   S C R E E N
    time.tick(Constants.fps)
    screen.fill(Colors.pleasant_red)
    screen.blit(font_arcade_120.render("Rabbunnies!", False, (255, 255, 255)), (170, 100))
    screen.blit(font_arcade_40.render("Press   Space   to   start!", False, (0, 0, 0)), (310, 400))
    screen.blit(font_arcade_40.render(help_msg_1, False, (0, 0, 0)), (320, 500))
    if not help_msg_2 == "":
        screen.blit(font_arcade_40.render(help_msg_2, False, (0, 0, 0)), (120, 550))
    if not help_msg_3 == "":
        screen.blit(font_arcade_40.render(help_msg_3, False, (0, 0, 0)), (270, 600))

    if pygame.key.get_pressed()[K_SPACE]:
        transition(Colors.pleasant_blue)
        break
    if pygame.key.get_pressed()[K_h]:
        help_msg_1 = "WASD  move    MOUSE   aim"
        help_msg_2 = "HOLD   CLICK   TO   CHARGE   BOMB    RELEASE    TO    THROW"
        help_msg_3 = "SCROLL   WHEEL   SELECT BOMB"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()

#                                                        M A I N   L O O P   I N I T I A L I Z E
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
        # This makes the info for each new collected bomb
        for indexForElem in range(0, len(Global.collected_bombs)):
            if Global.collected_bombs[indexForElem] == 1:
                Global.collected_bombs[indexForElem] = 2
                showInfo(indexForElem)
            indexForElem += 1

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
            if event.type == pygame.MOUSEBUTTONDOWN:    # this handles bomb selection during gameplay
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
        # activate and deactivate debug mode
        if pKey[K_o] and pKey[K_p] and pKey[K_i]:
            Global.Debug = True
        if pKey[K_j] and pKey[K_k] and [K_l]:
            Global.Debug = False
        # if player dies transition to GAME OVER screen
        if player.Health <= 0 and not Global.Debug:
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
            waveMinEnemies = int(Global.wave/3)+1
            waveMaxEnemies = int(Global.wave/2)+1
            if waveMinEnemies == waveMaxEnemies:
                waveMaxEnemies += 1
            for times in range(0, random.randrange(waveMinEnemies, waveMaxEnemies)):
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
    ObjectLists.listPickups = []
    Constants.scr_shake_offset_y = 0
    Constants.scr_shake_offset_x = 0
    scr.shakeAmmount = 0
    scr.shakeAmmountResolver = 0

    while True:     # GAME OVER SCREEN
        time.tick(Constants.fps)
        screen.fill(Colors.black)
        screen.blit(font_arcade_120.render("Game Over!", False, (255, 255, 255)), (250, 200))
        screen.blit(font_arcade_40.render("Score " + str(Global.score), False, (255, 255, 255)), (500-len(str(Global.score))*10, 400))
        screen.blit(font_arcade_40.render("Press   Space   to   restart!", False, (255, 255, 255)), (310, 500))

        if pygame.key.get_pressed()[K_SPACE]:
            transition(Colors.pleasant_blue)
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()

