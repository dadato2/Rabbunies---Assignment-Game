import sys, operator
from ExtClasses import *
from Debug import *
from Crosshair import *
from Player import *
from Enemy_Variants import *
from Bomb import *
from UI_Health import UI_Health
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

player = Player()
ObjectLists.listAllObjects.append(player)
crosshair = Crosshair()
ObjectLists.listAllObjects.append(crosshair)
healthUI = UI_Health()
ObjectLists.listUI.append(healthUI)

while True:     # T I T L E   S C R E E N
    time.tick(Constants.fps)
    screen.fill(Colors.red)
    screen.blit(pygame.font.SysFont('Comic Sans MS', 60).render("Rabbunnies!", False, (255, 255, 255)), (350, 100))
    screen.blit(pygame.font.SysFont('Comic Sans MS', 40).render("Press Space to start!", False, (0, 0, 0)), (310, 300))
    if pygame.key.get_pressed()[K_SPACE]:
        break
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()

nowTime = pygame.time.get_ticks()
lastTime = nowTime

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
    screen.fill(Colors.cyan)
    scr.update()
    for gameObject in ObjectLists.listAllObjects:
        gameObject.update()
        gameObject.draw(screen)
    for ui_object in ObjectLists.listUI:
        ui_object.update()
        ui_object.draw(screen)

    if len(ObjectLists.listOfEnemies) <= 0:
        for times in range(0, random.randrange(1, 4)):
            idd = random.randrange(3)
            if idd == 0:
                enemy = Bun1()
            elif idd == 1:
                enemy = Bun2()
            else:
                enemy = Bun3()
    screen.blit(Debug.debugtextsurface, (10, 10))
    screen.blit(pygame.font.SysFont('Comic Sans MS', 30).render("Enemies Left : " + str(len(ObjectLists.listOfEnemies)),
                                                                False, (0, 0, 0)), (10, Constants.scr_height - 50))
