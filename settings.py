class Settings():
    """"Класс для хранения всех настроек игры."""

    def __init__(self):
        """Инициализарует статические настройки игры."""
        # Параметы экрана
        self.screen_width = 1174
        self.screen_height = 910
        self.bg_color = (18, 16, 19)

        # Настройки корабля.
        self.ship_limit = 3

        # Настройки пришельцев.
        self.fleet_drop_speed = 100

        # Параметры пули
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 200, 0, 0
        self.bullets_allowed = 4

        # Темп ускорения игры.
        self.speedup_speed = 1.1

        # Темп роста стоимости пришельцев.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует изменяющиеся настройки игры"""
        self.ship_speed_factor = 4
        self.bullet_speed_factor = 6
        self.alien_speed_factor = 1

        # fleet_direction = 1 обозначает движение вправо, а -1 - влево.
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимости пришельцев."""
        self.ship_speed_factor *= self.speedup_speed
        self.bullet_speed_factor *= self.speedup_speed
        self.alien_speed_factor *= self.speedup_speed
        self.alien_points = int(self.alien_points* self.score_scale)
