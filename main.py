import pygame
import numpy as np
import random
from collections import deque

pygame.init()

WINDOW_SIZE = 500
GRID_SIZE = 10
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (0, 255, 0)
WALL = 2

window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Танчики")

# Инициализация сетки и позиции танчика
grid = np.zeros((GRID_SIZE, GRID_SIZE))
tank_pos = [GRID_SIZE // 2, GRID_SIZE // 2]
grid[tank_pos[0], tank_pos[1]] = 1  # Танк на старте

# Загрузка изображения танка
tank_image = pygame.image.load("serozhenka.png")
tank_image = pygame.transform.scale(tank_image, (CELL_SIZE, CELL_SIZE))

# Загрузка фона
background_image = pygame.image.load("fon.jpg")
background_image = pygame.transform.scale(background_image, (WINDOW_SIZE, WINDOW_SIZE))

# Параметры снарядов
bullets = []
bullet_speed = 1
last_direction = [0, 0]  # Направление последнего движения танка


def generate_walls():
    """Генерация стен, гарантируя, что танк сможет выехать"""
    # Заполнение поля случайными стенами
    grid_copy = np.zeros((GRID_SIZE, GRID_SIZE))
    num_walls = GRID_SIZE * GRID_SIZE // 4  # Например, 25% клеток заполним стенами

    for _ in range(num_walls):
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if x != tank_pos[0] or y != tank_pos[1]:  # Не ставить стену на танке
            grid_copy[x, y] = WALL

    # Проверяем, что есть путь от танка до других клеток
    if not is_reachable(grid_copy, tank_pos):
        return generate_walls()  # Рекурсивно пытаемся сгенерировать стены, если путь заблокирован

    return grid_copy


def is_reachable(fgrid, start_pos):
    """Проверка, что есть путь от стартовой позиции до других клеток"""
    visited = np.zeros_like(grid)
    queue = deque([start_pos])
    visited[start_pos[0], start_pos[1]] = 1

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Вверх, вниз, влево, вправо

    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx, ny] != WALL and visited[nx, ny] == 0:
                    visited[nx, ny] = 1
                    queue.append((nx, ny))

    # Если есть хотя бы одна непосещенная клетка, значит путь есть
    return np.any(visited)


# Генерация стен
grid = generate_walls()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    grid[tank_pos[0], tank_pos[1]] = 0
    moved = False

    if keys[pygame.K_w] and tank_pos[0] > 0 and grid[tank_pos[0] - 1, tank_pos[1]] != WALL:
        tank_pos[0] -= 1
        last_direction = [-1, 0]
        moved = True
    if keys[pygame.K_s] and tank_pos[0] < GRID_SIZE - 1 and grid[tank_pos[0] + 1, tank_pos[1]] != WALL:
        tank_pos[0] += 1
        last_direction = [1, 0]
        moved = True
    if keys[pygame.K_a] and tank_pos[1] > 0 and grid[tank_pos[0], tank_pos[1] - 1] != WALL:
        tank_pos[1] -= 1
        last_direction = [0, -1]
        moved = True
    if keys[pygame.K_d] and tank_pos[1] < GRID_SIZE - 1 and grid[tank_pos[0], tank_pos[1] + 1] != WALL:
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
    for bullet in bullets[:]:
        # Двигаем пулю в направлении ее движения
        bullet[0][0] += bullet[1][0] * bullet_speed
        bullet[0][1] += bullet[1][1] * bullet_speed

        # Проверяем, что пуля не вышла за пределы
        if not (0 <= bullet[0][0] < GRID_SIZE and 0 <= bullet[0][1] < GRID_SIZE):
            bullets.remove(bullet)  # Удаляем пулю, если она выходит за пределы поля

        # Проверяем столкновение с стеной
        elif grid[bullet[0][0], bullet[0][1]] == WALL:
            bullets.remove(bullet)  # Удаляем пулю, если она столкнулась с стеной

    # Отрисовка
    window.blit(background_image, (0, 0))  # Отображаем фон

    # Отрисовка сетки
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row, col] == 1:
                window.blit(tank_image, (col * CELL_SIZE, row * CELL_SIZE))
            elif grid[row, col] == WALL:
                pygame.draw.rect(window, (128, 128, 128), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка снарядов
    for bullet in bullets:
        pygame.draw.rect(window, YELLOW,
                         (bullet[0][1] * CELL_SIZE, bullet[0][0] * CELL_SIZE, CELL_SIZE // 4, CELL_SIZE // 4))

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
