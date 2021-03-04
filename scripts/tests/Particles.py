     
#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys, random
 
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
WINDOW_SIZE = (1920,1080)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

display = pygame.Surface((640,360),pygame.FULLSCREEN)


# [loc, velocity, timer]
particles = []
ParticleEffect = False
counter = 0
# Loop ------------------------------------------------------- #
while True:
    pygame.mouse.set_visible(False)
    # Background --------------------------------------------- #
    screen.fill((0,0,0))
    mx, my = pygame.mouse.get_pos()
    particles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(8, 10)])
    particles.append([[random.randint(0,1920), random.randint(0,1080)], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
    particles.append([[random.randint(0,1920), random.randint(0,1080)], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        pygame.draw.circle(screen, (144, 165, 169), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)
    
    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
          ParticleEffect = True
        if event.type == MOUSEBUTTONUP:
           ParticleEffect =False
                
    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)