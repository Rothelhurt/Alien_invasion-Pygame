import pygame.sysfont
from  pygame.sprite import Group

from ship_icon import ShipIcon


class Scoreboard():
    """Клас для вывода игровой информации."""
    def __init__(self, ai_settings, screen, stats):
        """Инициализирует атрибуты подсчета очков."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.ships = Group()

        # Настройка шрифта для вывода счета.
        self.text_color = (230, 230, 230)
        self.font = pygame.sysfont.SysFont(None, 48)
        # Подготовка исхоного изображения.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships_icon

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        rounded_score = round(self.stats.score, -1)
        score_str = '{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # Позиционирование счета в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = '{:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color,
                                                 self.ai_settings.bg_color)
        # Рекорд выравнивается по центру верхней стороны.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Преобразует номер уровня в графическое зиборажение."""
        self.level_image = self.font.render(str(self.stats.level),
                                            True, self.text_color,
                                            self.ai_settings.bg_color)

        # Уровень выводится под текущи счетом.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships_icon(self):
        """Сообщает количество оставшихся кораблей"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship_icon = ShipIcon(self.ai_settings, self.screen)
            ship_icon.rect.x = 10 + ship_number * ship_icon.rect.width
            ship_icon.rect.y = 10
            self.ships.add(ship_icon)

    def show_score(self):
        """Вывод счета, номера уровная, количество оставшихся кораблей на экран."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Отрисовка счетчика кораблей.
        self.ships.draw(self.screen)
