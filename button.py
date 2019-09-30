import pygame.sysfont


class Button():
    def __init__(self, ai_settings, screen, msg):
        """Инициализирует атрибуты кнопки."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Назаначение размеров и свойств кнопки.
        self.wight, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.sysfont.SysFont(None, 48)

        # Построение объекта rect кнопки и выравниванние по центру.
        self.rect = pygame.Rect(0, 0, self.wight, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создается один раз.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Преабразует msg в прямоугольник и выравнивает в текст по центру."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Отображение пустой кнопки и вывод сообщения.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
