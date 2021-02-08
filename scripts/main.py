import pygame, sys, time, random
import modules.player_character.player_character as player_character
import modules.engineFolder.engine as engine

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
bg = [-100,0]
flag = False
playJumpSound = True 
# game engine because it starts the game
def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

#attribues for the game engine class
game_map = load_map('Data/Game/frontTileMap')
grass_img= pygame.image.load('assets/backgrounds/tiles/grass.png')
dirt_img= pygame.image.load('assets/backgrounds/tiles/dirt.png')
bg_image= pygame.image.load('assets/backgrounds/bgs/bg hills.png').convert()
bg_image.set_colorkey((255,255,255))




def fallCheck():
    playerYChecker = ["0.6000000000000001","0.2","0.8","1.0","1.2","0.4"]
    for i in playerYChecker:
        i = float(i)
        if player_character1.vertical_momentum == i:
            return False
    return True

enemyRect = pygame.Rect(650, 0, 45, 45)
pygame.mixer.music.play()
while True: # game loop
    
    display.fill((146,244,255)) # clear screen by filling it with bluee
    pygame.draw.rect(display, (255,0,0), enemyRect)

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
    player_movement = [0,0]
    if player_character1.moving_right == True:
    
        player_movement[0] += 4
    if player_character1.moving_left == True:
        player_movement[0] -= 4
    player_movement[1] += player_character1.vertical_momentum
    player_character1.vertical_momentum += 0.2
    falling = fallCheck()

    if fallCheck():
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'fall')
        playJumpSound = False
    elif player_movement[0] >0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'run')
        player_character1.player_flip = False
    elif player_movement[0] ==0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'idle')
    elif player_movement[0] <0:
        player_character1.player_action,player_character1.player_frame =playerEngine.change_action(player_character1.player_action,player_character1.player_frame,'run')
        player_character1.player_flip = True
    playerPhysics.rect,collisions = playerPhysics.move(player_movement,tile_rects)
    if fallCheck() == False:
        playJumpSound = True

    if collisions['bottom'] == True:
        player_character1.air_timer = 0
        player_character1.vertical_momentum = 0
    else:
        player_character1.air_timer += 1
    if collisions['top']:
        player_character1.vertical_momentum += 2


    player_character1.player_frame += 1
    if player_character1.player_frame >= len(playerEngine.animation_database[player_character1.player_action]):
        player_character1.player_frame = 0
    player_img_id = playerEngine.animation_database[player_character1.player_action][player_character1.player_frame]
    player_img = playerEngine.animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_character1.player_flip,False),(playerPhysics.rect.x-scroll[0],playerPhysics.rect.y-scroll[1]))

    player_character1.moving_right,player_character1.moving_left,player_character1.vertical_momentum,flag = EventEngine.Eventchecker(player_character1.air_timer,player_character1.moving_right,player_character1.moving_left,player_character1.vertical_momentum,flag,jumping,playJumpSound)

    #print(player_character1.vertical_momentum)
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)

