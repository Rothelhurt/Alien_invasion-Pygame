import pygame
from pygame.sprite import Sprite


class ShipIcon(Sprite):
    def __init__(self, ai_settings, screen):
        """Инициализирует иконку кораблья"""
        super(ShipIcon, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # Загрузка изображения корабля и получение прямоугольника.
        self.image = pygame.image.load('images/ship_icon.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

    def blitme(self):
        """Рисует иконку корабля"""
        self.screen.blit(self.image, self.rect)
