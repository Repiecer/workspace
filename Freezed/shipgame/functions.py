import sys
import pygame
bgp = pygame.image.load('pictures/bg2.png')
def check_events(ship):#检测事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                ship.moving_right = True
            if event.key == pygame.K_a:
                ship.moving_left = True
            if event.key == pygame.K_w:
                ship.moving_up = True
            if event.key == pygame.K_s:
                ship.moving_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                ship.moving_right = False
            if event.key == pygame.K_a:
                ship.moving_left = False
            if event.key == pygame.K_w:
                ship.moving_up = False
            if event.key == pygame.K_s:
                ship.moving_down = False

def update_screen(settings, screen, ship):
    #screen.fill(settings.bg_color)
    screen.fill(settings.bg_color)
    screen.blit(bgp, (0, 0))
    ship.blitme()
    
    pygame.display.flip()
    