import sys
from random import randint
from time import sleep

import pygame

from star_sky import Star
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Реагирует на нажатие клавиш."""
    if event.key == pygame.K_RIGHT:
        # Перемещать корабль в право.
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        # Перемещать корабль в лево.
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, есди макситмум еще не достигнут."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""
    if event.key == pygame.K_RIGHT:
        # Прекратить перемещать корабль в право.
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        # Прекратить перемещать корабль в лево.
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """Отрабатывает нажатия клавиш и сорбытия мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                              bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки PLAY."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброс игровых настроек.
        ai_settings.initialize_dynamic_settings()

        # Указатель мыши скрывается после начла игры.
        pygame.mouse.set_visible(False)

        # Сброс игровой статистики.
        stats.reset_stats()
        stats.game_active = True

        # Осистка списка пуль и пришельцев.
        aliens.empty()
        bullets.empty()

        # Создание нового флота и возвашение корабля в центр.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, stars, ship, aliens, bullets,
                  play_button):
    """Обновляет изображения на экране и отоброжает новый экран."""
    # При каждой итерации цикла перерисовывает экран.
    screen.fill(ai_settings.bg_color)
    stars.draw(screen)
    # Все пули выводятся на экран поздаи изображения корабля.
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Кнопка Play отображается в том случае, если игра не активна.
    if not stats.game_active:
        play_button.draw_button()

    # Отображение последнего прорисованного экрана.
    pygame.display.flip()


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Обрабатывает столкновения корабля с пришельцами."""
    if stats.ships_left > 0:
        # Уменьшает количество короаблей.
        stats.ships_left -= 1

        # Отчистка пришельцев и пуль.
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_bullets(ai_settings, screen, stats, stars, ship, aliens, bullets,
                   play_button):
    """Обновляет позиции пуль и уничтожает старые пули."""
    # Обновление позиции пуль.
    bullets.update()
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, stars, ship, aliens, bullets,
                                  play_button)


def check_bullet_alien_collisions(ai_settings, screen, stats, stars, ship, aliens, bullets,
                                  play_button):
    """Обработка коллизий пуль с пришельцами."""
    # Удаление пуль и пришельцев, учавсвующих в колизиях.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # Уничтожение пуль, повышение сложности и создание нового флота.
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        ship.update()
        update_screen(ai_settings, screen, stats, stars, ship, aliens, bullets,
                      play_button)
        sleep(1.0)


def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверяет, добрались ли пришельци до нижнего края."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def create_star_sky(ai_settings, screen, stars):
    """Создает звездное небо"""
    star = Star(ai_settings, screen)
    number_stars_x = get_number_star_x(ai_settings, star.rect.width)
    number_stars_y = get_star_rows(ai_settings, star.rect.height)
    for star_number_y in range(number_stars_y):
        for star_number in range(number_stars_x):
            crate_star(ai_settings, screen, stars, star_number, star_number_y)


def get_number_star_x(ai_settings, star_width):
    available_space_x = ai_settings.screen_width - 50
    number_stars_x = int(available_space_x / (25 + star_width))
    return number_stars_x


def crate_star(ai_settings, screen, stars, star_number, star_number_y):
    star = Star(ai_settings, screen)
    star_width = star.rect.width
    star_height = star.rect.height
    star_rndm_x = randint(0, 25)
    star_rndm_y = randint(0, 25)
    star.x = 25 + (star_rndm_x + star_width) * star_number
    star.rect.x = star.x
    star.rect.y = 25 + (star_rndm_y + star_height) * star_number_y
    stars.add(star)


def get_star_rows(ai_settings, star_height):
    available_space_y = ai_settings.screen_height - 50
    number_stars_y = int(available_space_y / (25 + star_height))
    return number_stars_y


def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев"""
    # Создание пришельцев и вычисление количества пришельцев в ряду.

    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Создание флота пришельцев.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, number_rows):
    """Создает пришельца и размещает ео в ряду"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * number_rows
    aliens.add(alien)


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Обновляет позицию всех пришельцев во флоте."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Проверка коллизий пришельцев с кораблем.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение края пришельцем."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Снижает весь флот и меняет наравление."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
