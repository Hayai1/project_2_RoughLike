import pygame




class Enemy_character:
    #ATTRIBUTRES
    enemyId: int
    vertical_momentum: int
    moving_right: bool 
    moving_left: bool

    #CONSTRUCTOR    
    def __init__(self,enemyId):
        self.enemyId = enemyId
        self.moving_right = True
        self.moving_left = False
        self.vertical_momentum = 0
        self.enemy_movement = [0,0]
        self.enemy_flip = False
        self.enemyWaitCounter = 0
        self.aggro = False
         