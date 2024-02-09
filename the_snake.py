from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Основной класс"""

    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    body_color = (0, 0, 0)

    def __init__(self):
        pass

    def draw(self):
        """Докстринг"""
        pass


class Apple(GameObject):
    """Класс Яблока"""

    body_color = (255, 0, 0)
    position = (0, 0)

    def __init__(self):
        super().__init__()
        Apple.randomize_position(self)
        print(Apple.position)

    def randomize_position(self):
        """Докстринг"""
        x_pos = randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE
        y_pos = randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE
        Apple.position = (x_pos, y_pos)

    def draw(self, surface):
        """Метод draw класса Apple"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Змейка"""

    length = 1
    positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
    direction = RIGHT
    next_direction = None
    body_color = (0, 255, 0)

    def __init__(self):
        super().__init__()
        self.last = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Докстринг"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Ищем координаты головы"""
        return self.positions[0]

    def move(self):
        """Докстринг"""
        self.get_head_position()
        # print(self.get_head_position())
        if self.direction == RIGHT:
            self.positions.insert(0, (self.positions[0][0] + 20, self.positions[0][1]))
            self.last = self.positions[-1]
            self.positions.pop()
        elif self.direction == LEFT:
            self.positions.insert(0, (self.positions[0][0] - 20, self.positions[0][1]))
            self.last = self.positions[-1]
            self.positions.pop()
        elif self.direction == UP:
            self.positions.insert(0, (self.positions[0][0], self.positions[0][1] - 20))
            self.last = self.positions[-1]
            self.positions.pop()
        elif self.direction == DOWN:
            self.positions.insert(0, (self.positions[0][0], self.positions[0][1] + 20))
            self.last = self.positions[-1]
            self.positions.pop()
        #print(self.get_head_position())
        if self.length > len(self.positions):
            self.positions.append(self.last)
        for i in range(len(self.positions)):
            if self.positions[i][0] > 640:  # Выход за правую грань
                new_coord_x = self.positions[i][0] % 640
                tuple1 = self.positions[i]
                list1 = list(tuple1)
                list1[0] = new_coord_x
                tuple1 = tuple(list1)
                self.positions[i] = tuple1
            elif self.positions[i][0] < 0:  # Выход за левую грань
                new_coord_x = self.positions[i][0] % 640
                tuple1 = self.positions[i]
                list1 = list(tuple1)
                list1[0] = new_coord_x
                tuple1 = tuple(list1)
                self.positions[i] = tuple1
            elif self.positions[i][1] > 480:  # Выход за нижнюю грань
                new_coord_y = self.positions[i][1] % 480
                tuple1 = self.positions[i]
                list1 = list(tuple1)
                list1[1] = new_coord_y
                tuple1 = tuple(list1)
                self.positions[i] = tuple1
            elif self.positions[i][1] < 0:  # Выход за верхнюю грань
                new_coord_y = self.positions[0][1] % 480
                tuple1 = self.positions[i]
                list1 = list(tuple1)
                list1[1] = new_coord_y
                tuple1 = tuple(list1)
                self.positions[i] = tuple1

    def draw(self, surface):
        """Метод draw класса Snake"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        #     # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        #     # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Докстринг"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        list = [UP, DOWN, RIGHT, LEFT]
        self.direction = choice(list)
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:  # UP
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:  # DOWN
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:  # Left
                print('Нажали  направо')
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:  # Right
                game_object.next_direction = RIGHT
                print('Нажали  налево')


def main():
    """Основное тело"""
    # Тут нужно создать экземпляры классов.
    apple1 = Apple()
    snake1 = Snake()
    running = True

    while running:
        clock.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake1.direction != DOWN:  # UP
                    snake1.next_direction = UP
                elif event.key == pygame.K_DOWN and snake1.direction != UP:  # DOWN
                    snake1.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake1.direction != RIGHT:  # Left
                    snake1.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake1.direction != LEFT:  # Right
                    snake1.next_direction = RIGHT

        pygame.display.flip()

        apple1.draw(screen)
        snake1.draw(screen)
        snake1.update_direction()
        snake1.move()
        if snake1.positions[0] == apple1.position:  # Проверка на яблоко
            apple1 = Apple()
            snake1.length += 1
        if snake1.length > 6:  # Проверка на столкновение с собой
            for i in range(1, len(snake1.positions)):
                if snake1.positions[0] == snake1.positions[i]:
                    snake1.reset()

        # Тут опишите основную логику игры.
        # ...
        '''Обрабатывайте события клавиш при помощи функции handle_keys().
            Обновляйте направление движения змейки при помощи метода update_direction().
            Двигайте змейку (модифицируйте список) при помощи метода move().
            Проверяйте, съела ли змейка яблоко (если да, увеличьте длину змейки и переместите яблоко).
            Проверяйте столкновения змейки с собой (если столкновение, сброс игры при помощи метода reset()).
            Отрисовывайте змейку и яблоко, используя соответствующие методы draw.'''
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self, surface):
#     rect = pygame.Rect(
#         (self.position[0], self.position[1]),
#         (GRID_SIZE, GRID_SIZE)
#     )
#     pygame.draw.rect(surface, self.body_color, rect)
#     pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self, surface):
#     for position in self.positions[:-1]:
#         rect = (
#             pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
#         )
#         pygame.draw.rect(surface, self.body_color, rect)
#         pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(surface, self.body_color, head_rect)
#     pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(
#             (self.last[0], self.last[1]),
#             (GRID_SIZE, GRID_SIZE)
#         )
#         pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
