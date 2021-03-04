import pygame, sys, time, random, json


import modules.player_character.player_character as player_character
import modules.engineFolder.engine as engine
import modules.enemies.enemy_character as enemy_character
import modules.worldGen.Chunks  as Chunk_Module


clock = pygame.time.Clock()

from pygame.locals import *

pygame.init() # initiates pygame
pygame.mixer.init()

pygame.mixer.music.load("assets/audio/music/music 2.wav")
jumping = pygame.mixer.Sound("assets/audio/sounds/jump/jump.wav")
pygame.mixer.music.set_volume(1)
pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (1920,1080)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((640,360),pygame.FULLSCREEN) # used as the surface for rendering, which is scaled


playerEngine = engine.Engine(('assets/player_animations/run'),('assets/player_animations/idle'),('assets/player_animations/fall'),('assets/player_animations/land'),[7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7],[50])
player_character1 = player_character.Player_character()
playerPhysics = engine.PhysicsEngine(300,300,32,32,False,False)

lp = random.randint(1,1000000)
if lp == 21:
    print("lizzy eats potatoes")

#background attribute
true_scroll = [0,0] 
bg = [-50,0]
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
    
with open('data/game/gameMap.json') as f:
  data = json.load(f)

tilesets = ((data["levels"][0])["layerInstances"][0])["gridTiles"]
wallsets = ((data["levels"][0])["layerInstances"][1])["autoLayerTiles"]
enemyloc = load_map('data/game/enemyLoc')
def mapload(partpath,imgs):
    orientations = ('TL','TM','TR','ML','MM','MR','BL','BM','BR')
    for i in orientations:
        path = ('assets/backgrounds/'+ partpath + '/' + i +'.png')
        tileImage = pygame.image.load(path).convert()
        tileImage.set_colorkey((255,255,255))
        imgs.append(tileImage)
    return imgs
tiles_imgs=[]
tile_imgs = mapload('tiles',tiles_imgs)
wall_imgs=[]
wall_imgs = mapload('walls',wall_imgs)

tile_map = []
for tile in tilesets:
    location = tile["px"]
    imgType = tile["t"]
    tile_map.append([location,imgType])


tile_map = sorted(tile_map , key=lambda k: [k[0][0], k[0][1]])



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

incomingplayerLandAnim = False
def fallCheck(incomingplayerLandAnim):
    playerYChecker = ["0.6000000000000001","0.2","0.8","1.0","1.2","0.4"]
    for i in playerYChecker:
        i = float(i)
        if playerPhysics.vertical_momentum == i:
            return False,incomingplayerLandAnim
    incomingplayerLandAnim = True
    return True, incomingplayerLandAnim



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

pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()
counter = 0
chunk_rects = []
x= 0
y = 0
chunkCounter = 1
for ychunk in range(1,Chunk_Module.res[1]+1):
    y += 128
    x =0
    for xchunk in range(1,Chunk_Module.res[0]+1):
        chunk_rects.append([chunkCounter,[x, y, 128, 128],(random.randint(1,255),random.randint(1,255),random.randint(1,255))])
        x+=128
        chunkCounter += 1

box = pygame.Rect(-100, -100,840,660)

while True: # game loop
    display.fill((146,244,255)) # clear screen by filling it with blue
    #scrolling and background
    true_scroll[0] += (playerPhysics.rect.x-true_scroll[0]-200)/20
    true_scroll[1] += (playerPhysics.rect.y-true_scroll[1]-200)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    display.blit(bg_image,(bg[0]-scroll[0]*0.25,bg[1]-scroll[1]*0.25))
    for wall in wallsets:
            tileloc = wall["px"]
            wall_type = wall["t"]
            if wall_type == 6:
                display.blit(wall_imgs[0],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
            elif wall_type == 8:
                display.blit(wall_imgs[1],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
            elif wall_type == 10:
                display.blit(wall_imgs[2],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
            elif wall_type == 52:
                display.blit(wall_imgs[3],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
            elif wall_type == 54:
                display.blit(wall_imgs[4],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
            elif wall_type == 56:
                display.blit(wall_imgs[5],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
            elif wall_type == 98:
                display.blit(wall_imgs[6],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
            elif wall_type == 100:
                display.blit(wall_imgs[7],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
            elif wall_type == 102:
                display.blit(wall_imgs[8],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
    tile_rects = []
    for chunkrect in chunk_rects:
        crect = pygame.Rect(chunkrect[1][0]-scroll[0],chunkrect[1][1]-scroll[1],chunkrect[1][2],chunkrect[1][3])
        #pygame.draw.rect(display,(chunkrect[2]),crect)
        if box.colliderect(crect):
            for tile in Chunk_Module.chunks[int(chunkrect[0])]:
                tileloc = tile[0]
                tile_type = tile[1]
                if tile_type == 0:
                    display.blit(tiles_imgs[0],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
                    
                elif tile_type == 2:
                    display.blit(tiles_imgs[1],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
                    
                elif tile_type == 4:
                    display.blit(tiles_imgs[2],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
                    
                elif tile_type == 46:
                    display.blit(tiles_imgs[3],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
                    
                elif tile_type == 48:
                    display.blit(tiles_imgs[4],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
                    
                elif tile_type == 50:
                    display.blit(tiles_imgs[5],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
                    
                elif tile_type == 92:
                    display.blit(tiles_imgs[6],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
                    
                elif tile_type == 94:
                    display.blit(tiles_imgs[7],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
                    
                elif tile_type == 96:
                    
                    display.blit(tiles_imgs[8],(tileloc[0]-scroll[0],tileloc[1]-scroll[1]))
                tile_rects.append(pygame.Rect(tileloc[0],tileloc[1],16,16))

    EnemyWalls = []
    y = 0
    for layer in enemyloc:
        x = 0
        for tile in layer:
            if tile == '5':
                EnemyWalls.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1

    ########################################################################################################################       

    ########################################################################################################################
    #player animation coordinator
    playerPhysics.movement,playerPhysics.vertical_momentum = moving(playerPhysics.moving_right,playerPhysics.moving_left,playerPhysics.vertical_momentum,playerPhysics.movement)
    falling,incomingplayerLandAnim = fallCheck(incomingplayerLandAnim)
    if falling:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'fall')
        player_character1.playJumpSound = False
    elif incomingplayerLandAnim:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'land')
        incomingplayerLandAnim = False
    elif playerPhysics.movement[0] >0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'run')
        player_character1.player_flip = False
    elif playerPhysics.movement[0] ==0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'idle')
    elif playerPhysics.movement[0] <0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'run')
        player_character1.player_flip = True
    if fallCheck(incomingplayerLandAnim) == False:
        incomingplayerLandAnim = False 
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