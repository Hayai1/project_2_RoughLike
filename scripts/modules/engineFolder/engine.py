import pygame,sys,json
from pygame.locals import *
global animation_frames
animation_frames = {}
def load_animation(path,frame_durations):#path, [7,7,40]
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
            #print(animation_frames)
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n = int(n) 
            n += 1
        return animation_frame_data, animation_frames
        
class Engine:
    def __init__(self,runPath,idlePath,fallPath,runFrames,idleFrames,fallFrames):
        self.animation_database = {}
        self.runPath = runPath
        self.idlePath = idlePath
        self.fallPath = fallPath
        self.runFrames = runFrames
        self.idleFrames = idleFrames
        self.fallFrames = fallFrames
        self.animation_database['run'],self.animation_frames = load_animation(runPath,runFrames)
        self.animation_database['idle'],self.animation_frames = load_animation(idlePath,idleFrames)
        self.animation_database['fall'],self.animation_frames = load_animation(fallPath,fallFrames)
    



    def change_action(self,action_var,frame,new_value):
        if action_var != new_value:
            action_var = new_value
            frame =0
        return action_var,frame


def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def NonAggroEnemyMovement(movement,walls,rect,moving_left,moving_right,EnemyWaitCounter,waitTime,collision_types,wall):
    if movement[0] > 0:
        rect.right = wall.left
        collision_types['right'] = True
        if EnemyWaitCounter == waitTime:
            moving_right = False
            moving_left = True
            EnemyWaitCounter = 0
        else:
            EnemyWaitCounter += 1
    elif movement[0] < 0:
        rect.left = wall.right
        collision_types['left'] = True
        if EnemyWaitCounter == waitTime:
            moving_right = True
            moving_left = False
            EnemyWaitCounter = 0
        else:
            EnemyWaitCounter += 1
    return movement,walls,rect,moving_left,moving_right,EnemyWaitCounter,waitTime,collision_types
        

class PhysicsEngine:
    def __init__(self,x,y,x_size,y_size):
        self.width = x_size
        self.height = y_size
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.x = x
        self.y = y
        self.collisions_enemy: dict

    def move(self,movement,tiles,walls,rect,playerIndicator,air_timer,vertical_momentum,moving_left,moving_right,EnemyWaitCounter,waitTime):
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
        if playerIndicator == False:
            wall_list = collision_test(rect,walls)
            for wall in wall_list:
                movement,walls,rect,moving_left,moving_right,EnemyWaitCounter,waitTime,collision_types=NonAggroEnemyMovement(movement,tiles,rect,moving_left,moving_right,EnemyWaitCounter,waitTime,collision_types,wall)
        rect.y += movement[1]
        hit_list = collision_test(rect,tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        if playerIndicator == False:
            wall_list = collision_test(rect,walls)
            for wall in wall_list:
                if movement[1] > 0:
                    wall.bottom = wall.top
                    collision_types['bottom'] = True
            
                elif movement[1] < 0:
                    wall.top = wall.bottom
                    collision_types['top'] = True

        if collision_types['bottom']:
            vertical_momentum = 0
            air_timer = 0
        else:
            air_timer += 1
        if collision_types['top']:
            vertical_momentum += 2
        
        return rect,vertical_momentum,air_timer,moving_left,moving_right,collision_types,EnemyWaitCounter


def keyMap():
    f = open('data/config/input.json')
    data = json.load(f)
    keys = data["keys"][0]
    rightButton = ("K_"+keys["right"])
    leftButton = ("K_"+keys["left"])
    upButton = ("K_"+keys["up"])
    return rightButton,upButton,leftButton




keyMap()
class Events:
    def __init__(self):
        self.rightButton,self.upButton,self.leftButton = keyMap()

    def Eventchecker(self,air_timer,moving_right,moving_left,vertical_momentum,flag,jumping,playJumpSound):
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
                    if playJumpSound:
                        pygame.mixer.Sound.play(jumping)
                    if air_timer < 6:
                        vertical_momentum = -5
                        flag = True
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False
        return moving_right,moving_left,vertical_momentum,flag
                    
        



       