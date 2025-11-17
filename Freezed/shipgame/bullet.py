import pygame

class Bullet:
    def __init__(self, settings, ship) -> None:
        self.settings = settings
        self.ship = ship
        self.rect = pygame.Rect(self.ship.rect.centerx, self.ship.rect.centery, self.settings.bullet_width, self.settings.bullet_height)
        self.y = self.rect.centery

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.centery = self.y
