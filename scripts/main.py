import pygame, sys, time, random, json
import modules.player_character.player_character as player_character
import modules.engineFolder.engine as engine
import modules.enemies.enemy_character as enemy_character

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init() # initiates pygame
pygame.mixer.init()

pygame.mixer.music.load("assets/audio/music/music.wav")
jumping = pygame.mixer.Sound("assets/audio/sounds/jump/jump.wav")
pygame.mixer.music.set_volume(0.2)
pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (1920,1080)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((640,360),pygame.FULLSCREEN) # used as the surface for rendering, which is scaled


playerEngine = engine.Engine(('assets/player_animations/run'),('assets/player_animations/idle'),('assets/player_animations/fall'),[7,7,7,7],[7,7,7,7,7,7],[7,7,7])
player_character1 = player_character.Player_character()
playerPhysics = engine.PhysicsEngine(100,100,45,45,False,False)

lp = random.randint(1,1000000)
if lp == 21:
    print("lizzy eats potatoes")

#background attribute
true_scroll = [0,0] 
bg = [-100,-200]
flag = False
#enemy variables
# game engine because it starts the game
def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    map = []
    for row in data:
        map.append(list(row))
    return map


enemyloc = load_map('data/game/enemyLoc')
game_map = load_map('data/game/frontTileMap')
grass_img= pygame.image.load('assets/backgrounds/tiles/grass.png')
dirt_img= pygame.image.load('assets/backgrounds/tiles/dirt.png')
enemy_img= pygame.image.load('assets/Enemies/enemy1.png')
bg_image= pygame.image.load('assets/backgrounds/bgs/bg hills.png').convert()
bg_image.set_colorkey((255,255,255))
enemy_img.set_colorkey((255,255,255))

counter = 0 
y = 0
enemyAtrributesClasses = []
enemyPhysicsClasses = []
for i in enemyloc:
        x = 0
        for enemy in i:
            if enemy== '4':
                enemy = ("EnemyAtributes_"+str(counter))
                globals()[enemy] = enemy_character.Enemy_character(counter)
                enemyAtrributesClasses.append(globals()[enemy])
                enemy = ("EnemyPhysics_"+str(counter))
                globals()[enemy] = engine.PhysicsEngine(x*16,y*16,45,45,False,True)
                enemyPhysicsClasses.append(globals()[enemy])
                counter += 1
            else:
                pass
            x += 1
        y += 1


def fallCheck():
    playerYChecker = ["0.6000000000000001","0.2","0.8","1.0","1.2","0.4"]
    for i in playerYChecker:
        i = float(i)
        if playerPhysics.vertical_momentum == i:
            return False
    return True



def moving(moving_right,moving_left,vertical_momentum,movement):
    movement = [0,0]
    if moving_right == True:
    
        movement[0] += 4
    if moving_left == True:
        movement[0] -= 4
    movement[1] += vertical_momentum
    vertical_momentum += 0.2 
    return movement, vertical_momentum


def enmimMoving(moving_right,moving_left,vertical_momentum,movement):
    movement = [0,0]
    if moving_right == True:
    
        movement[0] += 1
    if moving_left == True:
        movement[0] -= 1
    movement[1] += vertical_momentum
    vertical_momentum += 0.2
    return movement, vertical_momentum



#pygame.mixer.music.play()
counter = 0
while True: # game loop
    display.fill((146,244,255)) # clear screen by filling it with bluee

    #scrolling and background
    true_scroll[0] += (playerPhysics.rect.x-true_scroll[0]-200)/20
    true_scroll[1] += (playerPhysics.rect.y-true_scroll[1]-200)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    display.blit(bg_image,(bg[0]-scroll[0]*0.25,bg[1]-scroll[1]*0.25))
    #displays tiles and creats rects for them
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '2':
                display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1
    EnemyWalls = []
    y = 0
    for layer in enemyloc:
        x = 0
        for tile in layer:
            if tile == '5':
                EnemyWalls.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1

    

    #player animation coordinator
    playerPhysics.movement,playerPhysics.vertical_momentum = moving(playerPhysics.moving_right,playerPhysics.moving_left,playerPhysics.vertical_momentum,playerPhysics.movement)
    
    if fallCheck():
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'fall')
        player_character1.playJumpSound = False
    elif playerPhysics.movement[0] >0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'run')
        player_character1.player_flip = False
    elif playerPhysics.movement[0] ==0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'idle')
    elif playerPhysics.movement[0] <0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'run')
        player_character1.player_flip = True
    if fallCheck() == False:
        player_character1.playJumpSound = True


 
    ignore = 0
    #player movement and collison check
    playerPhysics.rect,playerPhysics.vertical_momentum,player_character1.air_timer,ignore,ignore,ingore = playerPhysics.move(tile_rects,EnemyWalls,True,player_character1.air_timer,ignore,ignore)
    counter = 0
    for i in range(0,len(enemyAtrributesClasses)):
        waitTime =500
        EnemyPhysics=enemyPhysicsClasses[i]
        EnemyAtributes=enemyAtrributesClasses[i]
        EnemyPhysics.movement,EnemyPhysics.vertical_momentum = enmimMoving(EnemyPhysics.moving_right,EnemyPhysics.moving_left,EnemyPhysics.vertical_momentum,EnemyPhysics.movement)
        #enemy movement and collison check
        EnemyPhysics.rect,EnemyAtributes.vertical_momentum,ignore,EnemyAtributes.moving_left,EnemyAtributes.moving_right,EnemyAtributes.enemyWaitCounter = EnemyPhysics.move(tile_rects,EnemyWalls,False,0,EnemyAtributes.enemyWaitCounter,waitTime) 
        #enemy display
        if EnemyAtributes.moving_left:
            EnemyAtributes.enemy_flip = True
        else:
            EnemyAtributes.enemy_flip = False
        
        display.blit(pygame.transform.flip(enemy_img,EnemyAtributes.enemy_flip,False),(EnemyPhysics.rect.x-scroll[0],EnemyPhysics.rect.y-scroll[1]))
    
    #player display
    player_character1.player_frame += 1
    if player_character1.player_frame >= len(playerEngine.animation_database[player_character1.player_action]):
        player_character1.player_frame = 0
    player_img_id = playerEngine.animation_database[player_character1.player_action][player_character1.player_frame]
    player_img = playerEngine.animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_character1.player_flip,False),(playerPhysics.rect.x-scroll[0],playerPhysics.rect.y-scroll[1]))
    #events
    player_character1.moving_right,player_character1.moving_left,player_character1.vertical_momentum,flag = playerPhysics.Events(player_character1.air_timer,flag,jumping,player_character1.playJumpSound)          
    #clock / display/ displayupdate
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
