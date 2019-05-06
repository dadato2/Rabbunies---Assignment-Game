import sys, operator
from ExtClasses import *
from Debug import *
from Crosshair import *
from Player import *
from Enemy_Variants import *
from Bomb import *
from UI_Elements import UI_Health, UI_Enemies
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

font_arcade_40 = pygame.font.Font('assets/arcade.ttf', 40)
font_arcade_120 = pygame.font.Font('assets/arcade.ttf', 120)


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
        size_of_Circle = 1
        while True:
            if size_of_Circle >= Constants.scr_width:
                break
            size_of_Circle *= 1.1
            time.tick(Constants.fps)
            pygame.draw.circle(screen, Colors.pleasant_blue, (int(Constants.scr_width/2), int(Constants.scr_height/2)), int(size_of_Circle))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()
        break
    if pygame.key.get_pressed()[K_h]:
        help_msg_1 = "WASD  move    MOUSE   aim"
        help_msg_2 = "HOLD   CLICK   TO   CHARGE   BOMB    RELEASE    TO    THROW"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()

# M A I N   L O O P   I N I T I A L I Z E

player = Player()
ObjectLists.listAllObjects.append(player)
crosshair = Crosshair()
ObjectLists.listAllObjects.append(crosshair)
healthUI = UI_Health()
ObjectLists.listUI.append(healthUI)
enemyUI = UI_Enemies()
ObjectLists.listUI.append(enemyUI)

nowTime = pygame.time.get_ticks()
lastTime = nowTime
waitAMinute = 2

while True:                 # M A I N   L O O P
    nowTime = pygame.time.get_ticks()
    Time.deltaTime = (nowTime-lastTime) / 1000 % 1
    lastTime = nowTime
    time.tick(Constants.fps)
    pKey = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()

    if pKey[K_ESCAPE]:
        sys.exit()

    if player.Health <= 0:
        Debug.Log("Game Over")
    # else:
        # Debug.Log("Lives : " + str(player.Health))

    ObjectLists.listAllObjects.sort(key=operator.attrgetter('order'))
    ObjectLists.listUI.sort(key=operator.attrgetter('layer'))
    screen.fill(Colors.pleasant_blue)
    scr.update()
    for gameObject in ObjectLists.listAllObjects:
        gameObject.update()
        gameObject.draw(screen)
    for ui_object in ObjectLists.listUI:
        ui_object.update()
        ui_object.draw(screen)

    if waitAMinute > 0:
        waitAMinute -= Time.deltaTime
    if len(ObjectLists.listOfEnemies) <= 0 and waitAMinute <= 0:
        waitAMinute = random.randrange(1, 4)
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

