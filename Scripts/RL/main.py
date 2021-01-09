import pygame, sys, time

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # initiates pygame

pygame.display.set_caption('Pygame Platformer')

WINDOW_SIZE = (800,600)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((400,300)) # used as the surface for rendering, which is scaled

global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):#path, [7,7,40]
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        n = str(n) 
        animation_frame_id = animation_name + '_' + n
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n = int(n) 
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame =0
    return action_var,frame

animation_database = {}

animation_database['run'] = load_animation('assets/player_animations/run',[7,7,7])
animation_database['idle'] = load_animation('assets/player_animations/idle',[7,7,7])
animation_database['fall'] = load_animation('assets/player_animations/fall',[7,7])

player_action = 'idle'
player_frame = 0
player_flip = False

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

true_scroll = [0,0]

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('Data/Game/map')
grass_img= pygame.image.load('assets/backgrounds/tiles/grass.png')
dirt_img= pygame.image.load('assets/backgrounds/tiles/dirt.png')
bg_image= pygame.image.load('assets/backgrounds/bgs/bg hills.png').convert()
bg_image.set_colorkey((255,255,255))




player_rect= pygame.Rect(100,100,42,43)

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

bg = [-100,0]
flag = False
flag_2 = False
while True: # game loop
    display.fill((146,244,255)) # clear screen by filling it with blue

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
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
    if moving_right == True:
        player_movement[0] += 4
    if moving_left == True:
        player_movement[0] -= 4
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if flag_2:
        if vertical_momentum == 0.2:
            flag_2 = False
            flag = False
        else:
            flag = True
    if vertical_momentum > 5:
        vertical_momentum = 5

    if flag:
        player_action,player_frame =change_action(player_action,player_frame,'fall')
    elif player_movement[0] >0:
        player_action,player_frame =change_action(player_action,player_frame,'run')
        player_flip = False
    elif player_movement[0] ==0:
        player_action,player_frame =change_action(player_action,player_frame,'idle')
    elif player_movement[0] <0:
        player_action,player_frame =change_action(player_action,player_frame,'run')
        player_flip = True
    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1
    if collisions['top']:
        vertical_momentum += 2


    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                flag_2 = True
                if air_timer < 6:
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
