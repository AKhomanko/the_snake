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

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
STONE_COLOR = (96, 96, 96)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject():
    """Основной класс."""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = (0, 0, 0)

    def draw(self, screen, position, color=BOARD_BACKGROUND_COLOR,
             bord_color=BORDER_COLOR):
        """Метод draw класса Game."""
        rect = pg.Rect(
            position,
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, bord_color, rect, 1)


class Apple(GameObject):
    """Класс Яблока."""

    position = (0, 0)

    def __init__(self):
        # super().__init__()
        self.body_color = APPLE_COLOR
        self.posit = Snake.positions
        Apple.randomize_position(self)

    def randomize_position(self):
        """Вычисление позиции объекта."""
        x_pos = randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)
        y_pos = randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
        while (x_pos, y_pos) in Snake.positions:
            x_pos = randrange(0, SCREEN_WIDTH - GRID_SIZE, GRID_SIZE)
            y_pos = randrange(0, SCREEN_HEIGHT - GRID_SIZE, GRID_SIZE)
        self.position = (x_pos, y_pos)


class Stone(Apple):
    """Класс камня."""

    def __init__(self):
        self.body_color = STONE_COLOR
        # super().__init__()
        Stone.randomize_position(self)


class Snake(GameObject):
    """Класс Змейка."""

    length = 1
    position = (0, 0, 0)
    positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
    direction = RIGHT
    next_direction = None
    body_color = (0, 255, 0)

    def __init__(self):
        # super().__init__()
        self.last = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Ищем новое направление."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Ищем координаты головы."""
        return self.positions[0]

    def move(self):
        """Движение змейки."""
        self.get_head_position()
        if self.direction == RIGHT:
            self.positions.insert(
                0, (self.positions[0][0] + 20, self.positions[0][1]))
        elif self.direction == LEFT:
            self.positions.insert(
                0, (self.positions[0][0] - 20, self.positions[0][1]))
        elif self.direction == UP:
            self.positions.insert(
                0, (self.positions[0][0], self.positions[0][1] - 20))
        elif self.direction == DOWN:
            self.positions.insert(
                0, (self.positions[0][0], self.positions[0][1] + 20))
        self.last = self.positions.pop()

        if self.length > len(self.positions):
            self.positions.append(self.last)

        for i in range(len(self.positions)):
            if (self.positions[i][0] > SCREEN_WIDTH - GRID_SIZE
                    or self.positions[i][0] < 0):
                # Выход за грань по оси х
                new_coord_x = self.positions[i][0] % 640
                tuple1 = self.positions[i]
                list1 = list(tuple1)
                list1[0] = new_coord_x
                tuple1 = tuple(list1)
                self.positions[i] = tuple1

            if (self.positions[i][1] > SCREEN_HEIGHT - GRID_SIZE
                    or self.positions[i][1] < 0):
                # Выход за грань по оси у
                new_coord_y = self.positions[i][1] % 480
                tuple1 = self.positions[i]
                list1 = list(tuple1)
                list1[1] = new_coord_y
                tuple1 = tuple(list1)
                self.positions[i] = tuple1

    def draw(self, screen):
        """Метод draw класса Snake."""
        for self.position in self.positions:
            super().draw(screen, self.position, SNAKE_COLOR,)

        #     # Затирание последнего сегмента
        if self.last:
            super().draw(screen, self.last, bord_color=BOARD_BACKGROUND_COLOR)

    def reset(self):
        """Сбрасываем змейку при столкновении."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        list = [UP, DOWN, RIGHT, LEFT]
        self.direction = choice(list)
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основное тело."""
    pg.font.init()
    my_font = pg.font.SysFont('Comic Sans MS', 30)
    apple = Apple()
    snake = Snake()
    stone = Stone()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:  # столкновение с яблоком
            apple = Apple()
            snake.length += 1
        if snake.positions[0] == stone.position:  # столкновение с препятствием
            stone = Stone()
            snake.length -= 1
            snake.positions.pop()
            screen.fill((0, 0, 0))
        if snake.length > 4:  # Проверка на столкновение с собой
            if snake.positions[0] in snake.positions[1:]:
                snake.reset()

        text_surface = my_font.render(
            f'Ваш счёт:{snake.length-1}', False, (200, 0, 0), 20)
        screen.blit(text_surface, (0, 0))
        apple.draw(screen, apple.position, APPLE_COLOR)
        snake.draw(screen)
        stone.draw(screen, stone.position, STONE_COLOR)
        pg.display.update()
    pg.quit()


if __name__ == '__main__':
    main()
