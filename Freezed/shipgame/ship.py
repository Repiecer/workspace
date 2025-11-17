import pygame

class Ship():
    def __init__(self, screen, settings) -> None:
        self.screen = screen
        
        self.settings = settings
        self.image = pygame.image.load('pictures/kun2.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

    def update(self):
        if self.moving_right and self.rect.right < self.settings.screen_lengh:
            self.centerx +=self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.centerx -=self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.centery -=self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.settings.screen_height:
            self.centery +=self.settings.ship_speed
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
    def blitme(self):
        self.screen.blit(self.image, self.rect)