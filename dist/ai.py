import pygame
import random
from peremennie import GRID_SIZE, WALL



# Класс танка ИИ
class AI_Tank:
    def __init__(self, grid, tank_pos, tank_id, tank_image=None):
        self.grid = grid
        self.pos = tank_pos
        self.tank_id = tank_id  # ID танка для отличия от игрока
        self.last_direction = [0, 0]
        self.health = 3  # Начальное здоровье
        self.tank_image = tank_image if tank_image else pygame.image.load("sereozhaai.png")  # Изображение танка

    def move(self):
        """Рандомное движение для ИИ-танка"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Вверх, вниз, влево, вправо
        random.shuffle(directions)  # Случайный порядок направлений

        for dx, dy in directions:
            new_pos = [self.pos[0] + dx, self.pos[1] + dy]
            if 0 <= new_pos[0] < len(self.grid) and 0 <= new_pos[1] < len(self.grid[0]):
                if self.grid[new_pos[0]][new_pos[1]] == 0:  # Пустая клетка
                    self.pos = new_pos
                    self.last_direction = [dx, dy]
                    break

    def shoot(self, bullets, bullet_speed):
        """Стрельба по последней направленности"""
        bullet_pos = self.pos.copy()
        bullets.append([bullet_pos, self.last_direction])

    def update(self, bullets, bullet_speed):
        """Обновляем состояние ИИ-танка: движение и стрельба"""
        self.move()
        if random.random() < 1:  # 100% шанс на выстрел
            self.shoot(bullets, bullet_speed)

    def check_collision_with_bullet(self, bullet):
        """Проверка столкновения пули с танком"""
        if self.pos == bullet[0]:  # Если пуля попала в танк
            self.health -= 1  # Уменьшаем здоровье танка
            if self.health <= 0:  # Если здоровье танка стало 0, удаляем его
                return True  # Танк уничтожен
        return False