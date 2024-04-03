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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, body_color = None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color


    def draw(self):
        pass

class Apple(GameObject):
    def __init__(self):
        #self.body_color = APPLE_COLOR
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE,
        )

    def draw(self):
        rect = (pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    pass
    def __init__(self):
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        '''отвечает за обновление положения змейки в игре.'''
        head = self.get_head_position()

        dx, dy = self.direction
        new_pos_head = (head[0] + dx * GRID_SIZE, head[1] + dy * GRID_SIZE)
        
        new_pos_head = (new_pos_head[0] % SCREEN_WIDTH, new_pos_head[1] % SCREEN_HEIGHT)

        if new_pos_head in self.positions[2:]:
            reset()
        else:
            # Обновление списка позиций
            self.positions.insert(0, new_pos_head)
            if len(self.positions) > self.length:
                self.positions.pop()
            
    def reset(self):
        self.length = 1
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)



            
    def draw(self):

        for position in self.positions:
            # Используйте конструктор pygame.Rect для создания прямоугольника
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


    def get_head_position(self):
        return self.positions[0]



def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
    


def main():
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    apple.draw()
    snake = Snake()
    snake.draw()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        # ...
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        
        #handle_keys()
        snake.update_direction()
        snake.move()
        snake.draw()
        apple.draw()
        # apple.randomize_position()
        # apple.draw()
    
        pygame.display.update()

if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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