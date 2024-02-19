from random import choice, randrange

import pygame as pg

pg.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (173, 255, 47)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
STONE_COLOR = (128, 128, 128)
SNAKE_COLOR = (75, 0, 130)
WHITE = (255, 255, 255)
SPEED = 10

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surf1 = pg.Surface
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject():
    """Основной класс."""

    def __init__(self, bodycolor=BOARD_BACKGROUND_COLOR):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = bodycolor

    def draw(self, screen, position, color=BOARD_BACKGROUND_COLOR,
             bord_color=BORDER_COLOR):
        """Метод draw класса Game."""
        pass

    def draw_cell(self, screen, position, color=BOARD_BACKGROUND_COLOR,
                  bord_color=BORDER_COLOR):
        """Метод draw_cell класса Game."""
        rect = pg.Rect(
            position,
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, bord_color, rect, 1)


class Apple(GameObject):
    """Класс Яблока."""

    def __init__(self, bodycolor=APPLE_COLOR):
        super().__init__(bodycolor)
        self.body_color = bodycolor
        self.randomize_position(Snake)

    def randomize_position(self, obj):
        """Вычисление позиции объекта."""
        x = randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)
        y = randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
        while (x, y) in obj.positions:
            x = randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)
            y = randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
        self.position = (x, y)


class Snake(Apple):
    """Класс Змейка."""
    positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]

    def __init__(self, position=[((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]):
        super().__init__()
        self.reset()
        self.position = position

    def update_direction(self, next_direction):
        """Ищем новое направление."""
        if next_direction:
            self.direction = next_direction

    def get_head_position(self):
        """Ищем координаты головы."""
        return self.positions[0]

    def move(self, apple, stone):
        """Описание движения змейки."""
        head = self.get_head_position()
        head = (head[0] + self.direction[0] * GRID_SIZE,
                head[1] + self.direction[1] * GRID_SIZE)
        x, y = head
        x = x % SCREEN_WIDTH
        y = y % SCREEN_HEIGHT
        head = (x, y)
        self.positions.insert(0, head)

        if self.length != len(self.positions):  # Проверка на увеличение змейки
            self.last = self.positions.pop()

    def draw(self, screen):
        """Метод draw класса Snake."""
        head = self.get_head_position()
        self.draw_cell(screen, head, SNAKE_COLOR)
        if self.last:  # Затирание последнего сегмента
            self.draw_cell(screen, self.last,
                           bord_color=BOARD_BACKGROUND_COLOR)
        self.last = None

    def reset(self):
        """Сбрасываем змейку при столкновении."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        list = [UP, DOWN, RIGHT, LEFT]
        self.direction = choice(list)
        self.last = None
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def check_conflict(snake, apple, stone):
    """Функция обработки столкновений."""
    if snake.positions[0] == apple.position:  # столкновение с яблоком
        apple = Apple.randomize_position(apple, snake)
        snake.length += 1
    elif snake.positions[0] == stone.position:  # столкновение с камнем
        stone = Apple.randomize_position(stone, snake)
        snake.length -= 1
        snake.positions.pop()
        screen.fill(BOARD_BACKGROUND_COLOR)
    elif snake.length > 4:  # Проверка на столкновение с собой
        if snake.positions[0] in snake.positions[1:]:
            save_result(snake.length)
            snake.reset()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        dict_direction = {
            pg.K_UP: (UP, DOWN),
            pg.K_DOWN: (DOWN, UP),
            pg.K_LEFT: (LEFT, RIGHT),
            pg.K_RIGHT: (RIGHT, LEFT)}

        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key in dict_direction:
                if game_object.direction != dict_direction[event.key][1]:
                    game_object.next_direction = dict_direction[event.key][0]


def save_result(winner):
    """Обработка максимального результата для записи в файл"""
    with open('result.txt', 'r') as f:
        if int(f.read()) < winner:
            f1 = open('result.txt', 'w')
            winner = str(winner)
            f1.write(winner)


def main():
    """Основное тело."""
    pg.font.init()
    my_font = pg.font.SysFont('Comic Sans MS', 20)
    f = open('result.txt')
    best = f.read()
    snake = Snake()
    apple = Apple(APPLE_COLOR)
    stone = Apple(STONE_COLOR)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction(snake.next_direction)
        snake.move(apple, stone)
        check_conflict(snake, apple, stone)  # Проверка на столкновения
        text_surface = my_font.render(
            f'Ваш счёт:{snake.length-1}', False, (200, 0, 0),
            BOARD_BACKGROUND_COLOR)
        screen.blit(text_surface, (0, 0))      
        text_surface = my_font.render(
            f'Лучший результат:{best}', False, (200, 0, 0),
            BOARD_BACKGROUND_COLOR)
        screen.blit(text_surface, (200, 0))

        apple.draw_cell(screen, apple.position, APPLE_COLOR)
        stone.draw_cell(screen, stone.position, STONE_COLOR)
        snake.draw(screen)
        pg.display.update()
    pg.quit()


if __name__ == '__main__':
    main()
