from random import choice, randint

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = pygame.Color(0, 0, 0)

BORDER_COLOR = pygame.Color(93, 216, 228)

APPLE_COLOR = pygame.Color(255, 0, 0)

SNAKE_COLOR = pygame.Color(0, 255, 0)

SPEED = 20

DRCTN = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT
}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс"""

    def __init__(self, body_color=None):
        self.position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.body_color = body_color

    def draw(self):
        """Метод draw"""
        self.draw_cell()

    def draw_cell(self):
        """Метод для отрисовки"""
        rect = (pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс отвечающий за генерацию яблока"""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Метод для выбора рандомной позиции яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Вызов отрисовки из класса родителя"""
        super().draw_cell()


class Snake(GameObject):
    """Класс который отвечает за змейку"""

    def __init__(self):
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.position = self.positions[0]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновление направления"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        """отвечает за обновление положения змейки в игре."""
        head = self.get_head_position()

        dx, dy = self.direction
        new_pos_head_x, new_pos_head_y = (
            head[0] + dx * GRID_SIZE, head[1] + dy * GRID_SIZE
        )

        self.new_pos_head = (
            new_pos_head_x % SCREEN_WIDTH, new_pos_head_y % SCREEN_HEIGHT
        )

    def reset(self):
        """Возврат змейки на исходную"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Метод для отрисовки"""
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Метод возвращает голову змейки"""
        return self.positions[0]


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == DRCTN['up'] and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == DRCTN['down'] and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == DRCTN['left'] and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == DRCTN['right'] and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная логика игры"""
    snake = Snake()
    apple = Apple()
    apple.draw()
    snake.draw()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        snake.update_direction()
        snake.move(apple)

        if snake.new_pos_head in snake.positions[2:]:
            snake.reset()
        else:
            snake.positions.insert(0, snake.new_pos_head)
            if len(snake.positions) > snake.length:
                snake.positions.pop()
            if snake.new_pos_head == apple.position:
                snake.length += 1
                apple.randomize_position()

        if apple.position in snake.positions:
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
