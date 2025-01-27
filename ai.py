import random

class AI_Tank:
    def __init__(self, grid, tank_pos, tank_id):
        self.grid = grid
        self.pos = tank_pos
        self.tank_id = tank_id  # ID танка для отличия от игрока
        self.last_direction = [0, 0]
        self.health = 3  # Начальное здоровье

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
        if random.random() < 1:  # 10% шанс на выстрел
            self.shoot(bullets, bullet_speed)

    def check_collision_with_bullet(self, bullet):
        """Проверка столкновения пули с танком"""
        if self.pos == bullet[0]:
            self.health -= 1  # Уменьшаем здоровье танка
            return True
        return False
