import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
import game_functions as gf


def run_game():
    # Инициализация игры, создание объекта settings и screen.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Создание кнопки Play.
    play_button = Button(ai_settings, screen, 'Play')

    # Создание экземпляра для хранения статистики.
    stats = GameStats(ai_settings)

    # Создание группы звезд.
    stars = Group()
    gf.create_star_sky(ai_settings, screen, stars)
    # Создание Корабля.
    ship = Ship(ai_settings, screen)

    # Создание группы для хранения пуль.
    bullets = Group()

    # Создание пришельца, группы пришельцев.
    aliens = Group()

    # Создание флота пришельцев.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Запуск основгого цикла игры.
    while True:
        # Отслеживание событий клавиатуры и мыши.
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)

        if stats.game_active:
            # Обновить позицию коробля с учетом флагов.
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, stars, ship, aliens, bullets,
                      play_button)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
            # При каждой итерации цикла перерисовывает экран.
        gf.update_screen(ai_settings, screen, stats, stars, ship, aliens, bullets,
                         play_button)


run_game()
