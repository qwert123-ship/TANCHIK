import pygame
import numpy as np

pygame.init()

WINDOW_SIZE = 500
GRID_SIZE = 10
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Танчики")

# Инициализация сетки и позиции танчика
grid = np.zeros((GRID_SIZE, GRID_SIZE))
tank_pos = [GRID_SIZE // 2, GRID_SIZE // 2]
grid[tank_pos[0], tank_pos[1]] = 1

# Загрузка изображения танка
tank_image = pygame.image.load("serozhenka.png")
tank_image = pygame.transform.scale(tank_image, (CELL_SIZE, CELL_SIZE))

# Параметры снарядов
bullets = []
bullet_speed = 1
last_direction = [0, 0]  # Направление последнего движения танка

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    grid[tank_pos[0], tank_pos[1]] = 0
    moved = False

    if keys[pygame.K_w] and tank_pos[0] > 0:
        tank_pos[0] -= 1
        last_direction = [-1, 0]
        moved = True
    if keys[pygame.K_s] and tank_pos[0] < GRID_SIZE - 1:
        tank_pos[0] += 1
        last_direction = [1, 0]
        moved = True
    if keys[pygame.K_a] and tank_pos[1] > 0:
        tank_pos[1] -= 1
        last_direction = [0, -1]
        moved = True
    if keys[pygame.K_d] and tank_pos[1] < GRID_SIZE - 1:
        tank_pos[1] += 1
        last_direction = [0, 1]
        moved = True

    grid[tank_pos[0], tank_pos[1]] = 1

    # Проверка на нажатие клавиши "F" для выстрела
    if keys[pygame.K_f]:
        # Создание снаряда, который будет двигаться в последнем направлении
        bullet_pos = tank_pos.copy()
        bullets.append([bullet_pos, last_direction])

    # Обновление позиции снарядов
    for bullet in bullets:
        bullet[0][0] += bullet[1][0] * bullet_speed
        bullet[0][1] += bullet[1][1] * bullet_speed

    # Удаление снарядов, которые вышли за пределы экрана
    bullets = [bullet for bullet in bullets if
               0 <= bullet[0][0] < GRID_SIZE and 0 <= bullet[0][1] < GRID_SIZE]

    # Отрисовка
    window.fill(BLACK)  # Установить черный фон

    # Отрисовка сетки
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row, col] == 1:
                window.blit(tank_image, (col * CELL_SIZE, row * CELL_SIZE))

    # Отрисовка снарядов
    for bullet in bullets:
        pygame.draw.rect(window, YELLOW,
                         (bullet[0][1] * CELL_SIZE, bullet[0][0] * CELL_SIZE, CELL_SIZE // 4, CELL_SIZE // 4))

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
