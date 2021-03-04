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
    def __init__(self,runPath,idlePath,fallPath,landPath,runFrames,idleFrames,fallFrames,landFrames):
        self.animation_database = {}
        self.runPath = runPath
        self.idlePath = idlePath
        self.fallPath = fallPath
        self.landPath = landPath
        self.runFrames = runFrames
        self.idleFrames = idleFrames
        self.fallFrames = fallFrames
        self.landFrames = landFrames
        self.animation_database['run'],self.animation_frames = load_animation(runPath,runFrames)
        self.animation_database['idle'],self.animation_frames = load_animation(idlePath,idleFrames)
        self.animation_database['fall'],self.animation_frames = load_animation(fallPath,fallFrames)
        self.animation_database['land'],self.animation_frames = load_animation(landPath,landFrames)
    



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

def keyMap():
    f = open('data/config/input.json')
    data = json.load(f)
    keys = data["keys"][0]
    rightButton = ("K_"+keys["right"])
    leftButton = ("K_"+keys["left"])
    upButton = ("K_"+keys["up"])
    return rightButton,upButton,leftButton


        

class PhysicsEngine:
    def __init__(self,x,y,x_size,y_size,moving_left,moving_right):
        self.width = x_size
        self.height = y_size
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.x = x
        self.y = y
        self.movement = [0,0]
        self.vertical_momentum = 0
        self.moving_left = moving_left
        self.moving_right = moving_right


    def move(self,tiles,walls,playerIndicator,air_timer,EnemyWaitCounter,waitTime):
        collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        self.rect.x += self.movement[0]
        hit_list = collision_test(self.rect,tiles)

        for tile in hit_list:

            if self.movement[0] > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif self.movement[0] < 0:
                self.rect.left = tile.right
                collision_types['left'] = True
            
    
        if playerIndicator == False:
            wall_list = collision_test(self.rect,walls)
            for wall in wall_list:
                if self.movement[0] > 0:
                    self.rect.right = wall.left
                    collision_types['right'] = True
                    if EnemyWaitCounter == waitTime:
                        self.moving_right = False
                        self.moving_left = True
                        EnemyWaitCounter = 0
                    else:
                        EnemyWaitCounter += 1
                elif self.movement[0] < 0:
                    self.rect.left = wall.right
                    collision_types['left'] = True
                    if EnemyWaitCounter == waitTime:
                        self.moving_right = True
                        self.moving_left = False
                        EnemyWaitCounter = 0
                    else:
                        EnemyWaitCounter += 1


        self.rect.y += self.movement[1]
        hit_list = collision_test(self.rect,tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif self.movement[1] < 0:
                self.rect.top = tile.bottom
            
                collision_types['top'] = True
        if playerIndicator == False:
            wall_list = collision_test(self.rect,walls)
            for wall in wall_list:
                if self.movement[1] > 0:
                    wall.bottom = wall.top
                    collision_types['bottom'] = True
                elif self.movement[1] < 0:
                    wall.top = wall.bottom
                    collision_types['top'] = True

        if collision_types['bottom']:
            self.vertical_momentum = 0
            air_timer = 0
        else:
            air_timer += 1
        if collision_types['top']:
            self.vertical_momentum += 2
        
        return self.rect,self.vertical_momentum,air_timer,self.moving_left,self.moving_right,EnemyWaitCounter


    def Events(self,air_timer,flag,jumping,playJumpSound):
        for event in pygame.event.get(): # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.moving_right = True
                if event.key == K_LEFT:
                    self.moving_left = True
                if event.key == K_UP:
                    if playJumpSound:
                        pygame.mixer.Sound.play(jumping)
                    if air_timer < 6:
                        self.vertical_momentum = -5
                        flag = True
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.moving_right = False
                if event.key == K_LEFT:
                    self.moving_left = False
        return self.moving_right,self.moving_left,self.vertical_momentum,flag
                    






       