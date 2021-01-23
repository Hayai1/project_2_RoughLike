
class Player_character:
    #ATTRIBUTRES
    player_action: str
    player_frame: int 
    vertical_momentum: int
    air_timer: int 
    player_flip: bool
    moving_right: bool
    moving_left: bool
    #animation_database: dict
    player_rect: []
    
    

    #CONSTRUCTOR    
    def __init__(self, player_rect):
        self.player_rect = player_rect
        self.set_default_values()


    def set_default_values(self):
        self.player_action = 'idle'
        self.player_frame = 0 
        self.vertical_momentum = 0 
        self.air_timer = 0 
        self.player_flip = False 
        self.moving_right = False 
        self.moving_left = False
        # self.animation_database['run'] = load_animation('assets/player_animations/run',[7,7,7])
        # self.animation_database['idle'] = load_animation('assets/player_animations/idle',[7,7,7])
        # self.animation_database['fall'] = load_animation('assets/player_animations/fall',[7,7])
    
    # def animate(ad):
    #     self.player_frame += 1
    #     if self.player_frame >= len(animation_database[player_character1.player_action]):
    #     player_character1.player_frame = 0
    #     player_img_id = animation_database[player_character1.player_action][player_character1.player_frame]
    #     player_img = animation_frames[player_img_id]
    #     display.blit(pygame.transform.flip(player_img,player_character1.player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))
 