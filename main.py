
import pygame
import numpy as np
import random
from collections import deque
from ai import AI_Tank

print("WASD - ходьба, P - создание нового бота, O - пельмень-мод, J - старт ии")

pygame.init()

WINDOW_SIZE = 500
from peremennie import GRID_SIZE, WALL, bullet_speed
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (0, 255, 0)
hp = int(input("Количество хп: "))

window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Танчики")

# Инициализация сетки и позиции танчика
grid = np.zeros((GRID_SIZE, GRID_SIZE))
tank_pos = [GRID_SIZE // 2, GRID_SIZE // 2]
grid[tank_pos[0], tank_pos[1]] = 1  # Танк на старте

# Загрузка изображения танка
tank_image = pygame.image.load("serozhenka.png")
tank_image = pygame.transform.scale(tank_image, (CELL_SIZE, CELL_SIZE))

# Загрузка изображения для танков ИИ
ai_tank_image = pygame.image.load("sereozhaai.png")
ai_tank_image = pygame.transform.scale(ai_tank_image, (CELL_SIZE, CELL_SIZE))

# Загрузка фона
background_image = pygame.image.load("fon.jpg")
background_image = pygame.transform.scale(background_image, (WINDOW_SIZE, WINDOW_SIZE))

# Загрузка изображения пельменей
pelmeni_image = pygame.image.load("pelmeni.png")
pelmeni_image = pygame.transform.scale(pelmeni_image, (CELL_SIZE // 2, CELL_SIZE // 2))

# Параметры снарядов
bullets = []
last_direction = [0, 0]  # Направление последнего движения танка

# Переменная для хранения ввода текста
input_text = ""
pelmeni_mode = False # Флаг для переключения на пельмени
ai_mode = False  # Флаг для режима ИИ
ai_tanks = [AI_Tank(grid, [1, 1], 1), AI_Tank(grid, [GRID_SIZE - 2, GRID_SIZE - 2], 2)]

def generate_walls():
    """Генерация стен, гарантируя, что танк сможет выехать"""
    # Заполнение поля случайными стенами
    grid_copy = np.zeros((GRID_SIZE, GRID_SIZE))
    num_walls = GRID_SIZE * GRID_SIZE // 5  # НУ 1000 БУДЕТ НЕТ СТЕН ИЧО

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

def check_collision(pos, exclude_tank=None):
    """
    Проверяет, находится ли заданная позиция на танке (ИИ или игроке).
    :param pos: Позиция для проверки.
    :param exclude_tank: Исключить танк из проверки (например, если танк сам проверяет свою позицию).
    :return: True, если столкновение есть, иначе False.
    """
    # Проверяем столкновение с игроком
    if pos == tank_pos:
        return True

    # Проверяем столкновение с другими ИИ-танками
    for ai_tank in ai_tanks:
        if ai_tank != exclude_tank and ai_tank.pos == pos:
            return True

    return False

# Генерация стен
grid = generate_walls()

# Создание танков ИИ
ai_tanks = [AI_Tank(grid, [1, 1], 1), AI_Tank(grid, [GRID_SIZE - 2, GRID_SIZE - 2], 2)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:  # Нажатие "J" для включения/выключения режима ИИ
                ai_mode = not ai_mode  # Переключаем режим ИИ
            elif event.key == pygame.K_p:  # Добавление нового ИИ-танка при нажатии P
                # Генерация случайной позиции для нового ИИ-танка
                while True:
                    x = random.randint(0, GRID_SIZE - 1)
                    y = random.randint(0, GRID_SIZE - 1)
                    if grid[x, y] != WALL and grid[x, y] != 1:  # Убедиться, что это не стена и не место танка игрока
                        break
                # Создание нового танка ИИ
                new_tank = AI_Tank(grid, [x, y], len(ai_tanks) + 1)
                ai_tanks.append(new_tank)  # Добавление нового танка в список
            if event.key == pygame.K_BACKSPACE:
                # Удаление последнего символа при нажатии BACKSPACE
                input_text = input_text[:-1]
            elif event.key == pygame.K_o:
                # Если нажата клавиша Enter, проверяем введенный текст
                if event.key == pygame.K_o:  # Нажатие "O" для включения/выключения режима пельменей
                    pelmeni_mode = not pelmeni_mode  # Переключаем режим пельменей
                if event.key == pygame.K_BACKSPACE:
                    input_text = ""  # Очистить текст после обработки, понадобится в будущем для чит-команд



    keys = pygame.key.get_pressed()
    grid[tank_pos[0], tank_pos[1]] = 0
    moved = False

    if keys[pygame.K_w] and tank_pos[0] > 0 and grid[tank_pos[0] - 1, tank_pos[1]] != WALL:
        if not check_collision([tank_pos[0] - 1, tank_pos[1]]):
            tank_pos[0] -= 1
            last_direction = [-1, 0]
            moved = True
    if keys[pygame.K_s] and tank_pos[0] < GRID_SIZE - 1 and grid[tank_pos[0] + 1, tank_pos[1]] != WALL:
        if not check_collision([tank_pos[0] + 1, tank_pos[1]]):
            tank_pos[0] += 1
            last_direction = [1, 0]
            moved = True
    if keys[pygame.K_a] and tank_pos[1] > 0 and grid[tank_pos[0], tank_pos[1] - 1] != WALL:
        if not check_collision([tank_pos[0], tank_pos[1] - 1]):
            tank_pos[1] -= 1
            last_direction = [0, -1]
            moved = True
    if keys[pygame.K_d] and tank_pos[1] < GRID_SIZE - 1 and grid[tank_pos[0], tank_pos[1] + 1] != WALL:
        if not check_collision([tank_pos[0], tank_pos[1] + 1]):
            tank_pos[1] += 1
            last_direction = [0, 1]
            moved = True

    grid[tank_pos[0], tank_pos[1]] = 1

    # Проверка на нажатие клавиши "F" для выстрела
    if keys[pygame.K_f]:
        # Создание снаряда, который будет двигаться в последнем направлении
        bullet_pos = tank_pos.copy()
        bullets.append([bullet_pos, last_direction])

    # Если включен режим ИИ, обновляем движение ИИ-танков
    if ai_mode:
        for ai_tank in ai_tanks:
            ai_tank.update(bullets, bullet_speed)  # Каждый ИИ-танк стреляет и двигается

    # Обновление позиции снарядов
    for bullet in bullets[:]:
        # Двигаем пулю в направлении ее движения
        bullet[0][0] += bullet[1][0] * bullet_speed
        bullet[0][1] += bullet[1][1] * bullet_speed


        # Проверяем, что пуля не вышла за пределы
        if not (0 <= bullet[0][0] < GRID_SIZE and 0 <= bullet[0][1] < GRID_SIZE):
            bullets.remove(bullet)  # Удаляем пулю, если она выходит за пределы
        # Проверка столкновения с стеной
        elif grid[bullet[0][0], bullet[0][1]] == WALL:
            bullets.remove(bullet)  # Удаляем пулю, если она столкнулась со стеной

        else:
            # Проверка столкновения с игроком
            if 0 <= bullet[0][0] < GRID_SIZE and 0 <= bullet[0][1] < GRID_SIZE:
                if grid[bullet[0][0], bullet[0][1]] == 1:  # Если пуля попала в игрока
                    grid[bullet[0][0], bullet[0][1]] = 0  # Удаляем танк игрока
                    # Можете добавить сюда логику для уменьшения здоровья игрока или окончания игры
                    if tank_pos == bullet[0]:
                        hp -= 1  # Уменьшаем здоровье танка
                        if hp <= 0:
                            print("Вы проиграли")
                            pygame.quit()

            # Проверка столкновений с танками ИИ
            for ai_tank in ai_tanks:
                if ai_tank.check_collision_with_bullet(bullet):
                    bullets.remove(bullet)  # Удаляем пулю при попадании
                    if ai_tank.health <= 0:
                        ai_tanks.remove(ai_tank)  # Удаляем танк ИИ, если его здоровье 0
                    break

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
        if pelmeni_mode:
            # Если пельмени, рисуем их
            window.blit(pelmeni_image, (bullet[0][1] * CELL_SIZE, bullet[0][0] * CELL_SIZE))
        else:
            pygame.draw.rect(window, YELLOW, (bullet[0][1] * CELL_SIZE, bullet[0][0] * CELL_SIZE, CELL_SIZE // 4, CELL_SIZE // 4))

    # Отрисовка ИИ-танков
    for ai_tank in ai_tanks:
        window.blit(ai_tank_image, (ai_tank.pos[1] * CELL_SIZE, ai_tank.pos[0] * CELL_SIZE))

    if GRID_SIZE >= 100:
        print("суссище, меньше 100 ставь")
        pygame.quit()
        quit()

    if hp >= 20:
        print("читер")
        quit()

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()