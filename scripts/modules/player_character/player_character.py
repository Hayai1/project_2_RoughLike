import pygame




class Player_character:
    #ATTRIBUTRES
    player_action: str
    player_frame: int 
    vertical_momentum: int
    air_timer: int 
    player_flip: bool
    moving_right: bool
    moving_left: bool
    
    

    #CONSTRUCTOR    
    def __init__(self):
        self.set_default_values()


    def set_default_values(self):
        self.player_action = 'idle'
        self.player_frame = 0 
        self.vertical_momentum = 0 
        self.air_timer = 0 
        self.player_flip = False 
        self.moving_right = False 
        self.moving_left = False
        self.playJumpSound = True 
        self.player_movement = [0,0]
 