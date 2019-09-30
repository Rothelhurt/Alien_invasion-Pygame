class GameStats():
    """Отслеживание статистики игры."""
    def __init__(self, ai_settings):
        """Ининициализирует статистику"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Игра запускается в неактивном состоянии.
        self.game_active = False

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ships_left = self.ai_settings.ship_limit
