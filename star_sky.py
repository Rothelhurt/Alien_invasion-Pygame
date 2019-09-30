import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """Класс, представляющий фрагмент звездного неба."""
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения звездного неба и назначение rect.
        self.image = pygame.image.load('images/black.png')
        self.rect = self.image.get_rect()

        # Каждый новый фрагмент звездного неба
        # появляется в верхнем левом углу экрана.
        self.rect.x = 20
        self.rect.y = 20

        # Сохранение точной позиции фрагмента звездного неба.
        self.x = float(self.rect.x)

    def blitme(self):
        """Выводит фрагмент звездного неба в текущем положении."""
        self.screen.blit(self.image, self.rect)
