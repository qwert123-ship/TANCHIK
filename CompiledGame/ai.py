import pygame
import random
from peremennie import GRID_SIZE, WALL



# Класс танка ИИ
class AI_Tank:
    def __init__(self, grid, pos, tank_id):
        self.grid = grid
        self.pos = pos
        self.tank_id = tank_id
        self.health = 5  # Начальное здоровье танка ИИ

        # Загружаем изображение танка
        self.image = pygame.image.load("sereozhaai.png")  # Используем гарантированное изображение
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))  # Масштабируем изображение

    def move(self, bullets):
        """Двигает танк ИИ случайным образом"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Вверх, вниз, влево, вправо
        random.shuffle(directions)  # Перемешиваем направления для случайного движения

        for dx, dy in directions:
            nx, ny = self.pos[0] + dx, self.pos[1] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if self.grid[nx, ny] != WALL:  # Если клетка не занята стеной
                    self.pos = [nx, ny]
                    break

    def shoot(self):
        """Танк ИИ стреляет"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Вверх, вниз, влево, вправо
        random_direction = random.choice(directions)  # Выбираем случайное направление для выстрела
        bullet_pos = self.pos.copy()
        bullet_direction = random_direction
        return [bullet_pos, bullet_direction]  # Возвращаем пульку с позицией и направлением

    def update(self, bullets, bullet_speed):
        """Обновляет поведение ИИ-танка"""
        self.move(bullets)  # Двигаем танк ИИ
        if random.random() < 1:  # 10% шанс на выстрел
            bullet = self.shoot()
            bullets.append(bullet)  # Добавляем пулю в список пуль

    def check_collision_with_bullet(self, bullet):
        """Проверяет столкновение с пулей"""
        bullet_x, bullet_y = bullet[0][0], bullet[0][1]
        if self.pos[0] == bullet_x and self.pos[1] == bullet_y:
            return True  # Если пуля попала в танк, возвращаем True
        return False