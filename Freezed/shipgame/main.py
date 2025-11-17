import pygame

from settings import Settings
from ship import Ship
import functions as fg

def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_lengh, settings.screen_height))
    ship = Ship(screen, settings)
    pygame.display.set_caption("test")
    bgp = pygame.image.load('pictures/bg2.png')
    while True:
        fg.check_events(ship)
        ship.update()
        fg.update_screen(settings, screen, ship)


run_game()
