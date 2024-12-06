import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("почти копия контр страйка")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Персонаж игрока
player_size = 50
player = pygame.Rect(100, HEIGHT - player_size - 50, player_size, player_size)
player_color = GREEN
player_velocity_y = 0
gravity = 0.5
jump_power = -10
on_ground = True

# Враги
enemy_size = 50
enemies = []
enemy_spawn_timer = 0
enemy_speed = 20

# Снаряды
bullets = []
bullet_speed = 30

# Счёт и жизни
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Прыжок игрока
            if event.key == pygame.K_SPACE and on_ground:
                player_velocity_y = jump_power
                on_ground = False
            # Стрельба
            if event.key == pygame.K_f:
                bullets.append(pygame.Rect(player.x + player.width, player.y + player.height // 2 - 5, 10, 5))

    # Логика игрока
    player_velocity_y += gravity
    player.y += player_velocity_y

    # Проверка, чтобы игрок не проваливался ниже земли
    if player.y + player.height >= HEIGHT - 50:
        player.y = HEIGHT - 50 - player.height
        player_velocity_y = 0
        on_ground = True

    # Логика врагов
    enemy_spawn_timer += 1
    if enemy_spawn_timer > random. randint(10, 600):  # Добавляем нового врага через элемент рандом
        enemies.append(pygame.Rect(WIDTH, HEIGHT - enemy_size - 50, enemy_size, enemy_size))
        enemy_spawn_timer = 0

    for enemy in enemies:
        enemy.x -= enemy_speed
        # Если враг вышел за экран, убираем его и отнимаем жизнь
        if enemy.x + enemy.width < 0:
            enemies.remove(enemy)
            lives -= 1

    # Логика снарядов
    for bullet in bullets:
        bullet.x += bullet_speed
        # Удаляем снаряды, которые покидают экран
        if bullet.x > WIDTH:
            bullets.remove(bullet)
            lives -= 1

    # Проверка на попадание снарядов во врагов
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10
                break

    # Конец игры, если у игрока закончились жизни
    if lives <= 0:
        running = False
        print("Игра окончена! Ваш счёт:", score)

    # Отрисовка экрана
    screen.fill(WHITE)

    # Рисуем игрока
    pygame.draw.rect(screen, player_color, player)

    # Рисуем врагов
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # Рисуем снаряды
    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet)

    # Рисуем интерфейс: счёт и количество жизней
    score_text = font.render(f"Очки: {score}", True, BLACK)
    lives_text = font.render(f"Жизни: {lives}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

# Завершение работы
pygame.quit()
