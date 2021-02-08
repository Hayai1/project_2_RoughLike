import pygame




class Enemy_character:
    #ATTRIBUTRES
    enemy_action: str
    enemy_frame: int
    enemy_flip: bool
    moving_right: bool
    moving_left: bool
    
    

    #CONSTRUCTOR    
    def __init__(self):
        self.set_default_values()


    def set_default_values(self):
        self.enemy_action = 'walk'
        self.enemy_frame = 0
        self.enemy_flip = False
        self.moving_right = False
        self.moving_left = False 
 