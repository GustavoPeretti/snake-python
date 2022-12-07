import pygame
from pygame.locals import *
from sys import exit
from random import randint

green = '#228b22'
white = '#FFFFFF'
black = '#000000'
red = '#FF0000'

screen_size = (800, 800)
grid_size = 20
space_size = screen_size[0] // 20

pygame.init()

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Snake')
pygame.display.set_icon(pygame.image.load(r'img\snake.png'))
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.snake_color = white
        self.pos = [5, 10]
        self.queue = [self.pos, [4, 10]]
        self.orientation = 'E'

    def move(self):
        new_queue = []
        for p in range(len(self.queue)):
            if p == 0:
                if self.orientation == 'N':
                    new_queue.append([self.pos[0], self.pos[1] - 1])
                elif self.orientation == 'S':
                    new_queue.append([self.pos[0], self.pos[1] + 1])
                elif self.orientation == 'W':
                    new_queue.append([self.pos[0] - 1, self.pos[1]])
                else:
                    new_queue.append([self.pos[0] + 1, self.pos[1]])
            else:
                new_queue.append(self.queue[p - 1])
        self.queue = new_queue
        self.pos = self.queue[0]

    def draw(self):
        for s in self.queue:
            rectangle = pygame.Rect(s[0] * space_size, s[1] * space_size, space_size, space_size)
            pygame.draw.rect(screen, self.snake_color, rectangle)
            self.draw_eyes()

    def draw_eyes(self):
        if screen_size[0] >= 800:
            coord = self.pos[0] * space_size, self.pos[1] * space_size
            if self.orientation == 'N':
                rectangle = pygame.Rect(coord[0] + 4, coord[1], 4, 4)
                pygame.draw.rect(screen, black, rectangle)
                rectangle = pygame.Rect(coord[0] + 32, coord[1], 4, 4)
            elif self.orientation == 'S':
                rectangle = pygame.Rect(coord[0] + 4, coord[1] + 36, 4, 4)
                pygame.draw.rect(screen, black, rectangle)
                rectangle = pygame.Rect(coord[0] + 32, coord[1] + 36, 4, 4)
            elif self.orientation == 'W':
                rectangle = pygame.Rect(coord[0], coord[1] + 4, 4, 4)
                pygame.draw.rect(screen, black, rectangle)
                rectangle = pygame.Rect(coord[0], coord[1] + 32, 4, 4)
            else:
                rectangle = pygame.Rect(coord[0] + 36, coord[1] + 4, 4, 4)
                pygame.draw.rect(screen, black, rectangle)
                rectangle = pygame.Rect(coord[0] + 36, coord[1] + 32, 4, 4)
            pygame.draw.rect(screen, black, rectangle)

    def grow(self):
        self.queue.append(self.queue[len(self.queue) - 1])


class Food:
    def __init__(self, snake):
        self.pos = [randint(0, grid_size - 1), randint(0, grid_size - 1)]
        while self.pos in snake.queue:
            self.pos = [randint(0, grid_size - 1), randint(0, grid_size - 1)]
        self.color = red

    def draw(self):
        rectangle = pygame.Rect(self.pos[0] * space_size, self.pos[1] * space_size, space_size, space_size)
        pygame.draw.rect(screen, self.color, rectangle)


snake = Snake()
food = Food(snake)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_UP and snake.orientation != 'S':
                snake.orientation = 'N'
            if event.key == K_DOWN and snake.orientation != 'N':
                snake.orientation = 'S'
            if event.key == K_LEFT and snake.orientation != 'E':
                snake.orientation = 'W'
            if event.key == K_RIGHT and snake.orientation != 'W':
                snake.orientation = 'E'
            if event.key == K_SPACE:
                snake.grow()
    if any(not 0 <= n < grid_size for pos in snake.queue for n in pos) or \
            any(snake.queue.count(pos) > 1 for pos in snake.queue):
        pygame.quit()
        exit()
    screen.fill(green)
    if snake.pos == food.pos:
        food = Food(snake)
        snake.grow()
    snake.move()
    food.draw()
    snake.draw()
    pygame.display.flip()
    clock.tick(8)
    pygame.display.update()
