import sys, operator
from ExtClasses import *
from Debug import *
from Crosshair import *
from Player import *
from Bomb import *
from ScreenControl import ScreenController

lastTime = 0
nowTime = 0


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

# roomImage = pygame.image.load("assets/room.png").convert()


player = Player()
ObjectLists.listAllObjects.append(player)
crosshair = Crosshair()
ObjectLists.listAllObjects.append(crosshair)

# cube = Bomb()
# cube.x, cube.y = 360, 360


while True:                 # M A I N   L O O P

    nowTime = pygame.time.get_ticks()
    Time.deltaTime = (nowTime-lastTime) / 1000
    lastTime = nowTime
    time.tick(Constants.fps)
    pKey = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()
    # screen.blit(roomImage, (0, 0))
    # if pKey[K_ESCAPE]:
       #  sys.exit()
    if pKey[K_SPACE]:
        scr.shakeScreen(5, 1)
    if Constants.enemycount <= 0:
        Debug.Log(crosshair.xy)
    else:
        Debug.Log(Constants.enemycount)

    ObjectLists.listAllObjects.sort(key=operator.attrgetter('order'))
    screen.fill(Colors.cyan)
    scr.update()
    for gameObject in ObjectLists.listAllObjects:
        gameObject.update()
        gameObject.draw(screen)

    screen.blit(Debug.debugtextsurface, (10, 10))
