import pygame, sys, time, random
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
playerPhysics = engine.PhysicsEngine(100,100,45,45)
EventEngine = engine.Events()

lp = random.randint(1,1000000)
if lp == 21:
    print("lizzy eats potatoes")

#background attribute
true_scroll = [0,0] 
bg = [-100,-200]
flag = False
#enemy variables
waitTime =500
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


#attribues for the game engine class
enemyloc = load_map('data/game/enemyLoc')
game_map = load_map('data/game/frontTileMap')
grass_img= pygame.image.load('assets/backgrounds/tiles/grass.png')
dirt_img= pygame.image.load('assets/backgrounds/tiles/dirt.png')
enemy_img= pygame.image.load('assets/Enemies/Relicsan.png')
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
                globals()[enemy] = engine.PhysicsEngine(x*16,y*16,45,45)
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
        if player_character1.vertical_momentum == i:
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


    true_scroll[0] += (playerPhysics.rect.x-true_scroll[0]-200)/20
    true_scroll[1] += (playerPhysics.rect.y-true_scroll[1]-200)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    display.blit(bg_image,(bg[0]-scroll[0]*0.25,bg[1]-scroll[1]*0.25))
    
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

    

    
    player_character1.player_movement,player_character1.vertical_momentum = moving(player_character1.moving_right,player_character1.moving_left,player_character1.vertical_momentum,player_character1.player_movement)
    for EnemyAtributes in enemyAtrributesClasses:
        EnemyAtributes.enemy_movement,EnemyAtributes.vertical_momentum = enmimMoving(EnemyAtributes.moving_right,EnemyAtributes.moving_left,EnemyAtributes.vertical_momentum,EnemyAtributes.enemy_movement)
    if fallCheck():
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'fall')
        player_character1.playJumpSound = False
    elif player_character1.player_movement[0] >0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'run')
        player_character1.player_flip = False
    elif player_character1.player_movement[0] ==0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'idle')
    elif player_character1.player_movement[0] <0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'run')
        player_character1.player_flip = True
    if fallCheck() == False:
        player_character1.playJumpSound = True


 
    unused1 = 0  
    unused2 = 0
    playerPhysics.rect,player_character1.vertical_momentum,player_character1.air_timer,unused1,unused2,collision_types,null = playerPhysics.move(player_character1.player_movement,tile_rects,EnemyWalls,playerPhysics.rect,True,player_character1.air_timer,player_character1.vertical_momentum,unused1,unused2,0,0,EnemyAtributes.aggro)
    del unused1,unused2,null
    counter = 0
    for i in range(0,len(enemyAtrributesClasses)):
        EnemyPhysics=enemyPhysicsClasses[i]
        EnemyAtributes=enemyAtrributesClasses[i]
        EnemyPhysics.rect,EnemyAtributes.vertical_momentum,var,EnemyAtributes.moving_left,EnemyAtributes.moving_right,collision_types,EnemyAtributes.enemyWaitCounter = EnemyPhysics.move(EnemyAtributes.enemy_movement,tile_rects,EnemyWalls,EnemyPhysics.rect,False,0,EnemyAtributes.vertical_momentum,EnemyAtributes.moving_left,EnemyAtributes.moving_right,EnemyAtributes.enemyWaitCounter,waitTime,EnemyAtributes.aggro) 
        del var

    player_character1.player_frame += 1
    if player_character1.player_frame >= len(playerEngine.animation_database[player_character1.player_action]):
        player_character1.player_frame = 0
    player_img_id = playerEngine.animation_database[player_character1.player_action][player_character1.player_frame]
    player_img = playerEngine.animation_frames[player_img_id]
    for i in range(0,len(enemyAtrributesClasses)):
        EnemyPhysics=enemyPhysicsClasses[i]
        EnemyAtributes=enemyAtrributesClasses[i]

        if EnemyPhysics.rect.x + 1000 < playerPhysics.rect.x or EnemyPhysics.rect.x - 1000 < playerPhysics.rect.x :
            EnemyAtributes.aggro = True
        if EnemyAtributes.moving_left:
            EnemyAtributes.enemy_flip = True
        else:
            EnemyAtributes.enemy_flip = False
        display.blit(pygame.transform.flip(enemy_img,EnemyAtributes.enemy_flip,False),(EnemyPhysics.rect.x-scroll[0],EnemyPhysics.rect.y-scroll[1]))
    display.blit(pygame.transform.flip(player_img,player_character1.player_flip,False),(playerPhysics.rect.x-scroll[0],playerPhysics.rect.y-scroll[1]))

    player_character1.moving_right,player_character1.moving_left,player_character1.vertical_momentum,flag = EventEngine.Eventchecker(player_character1.air_timer,player_character1.moving_right,player_character1.moving_left,player_character1.vertical_momentum,flag,jumping,player_character1.playJumpSound)
                

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)

