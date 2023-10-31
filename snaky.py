import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 640, 480
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 128, 255) 

# Define the snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.color = BLUE

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction

        new = (((cur[0] + (x * 20)) % WIDTH), (cur[1] + (y * 20)) % HEIGHT)

        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.size:
                self.positions.pop()

    def reset(self):
        self.size = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

    def render(self):
        for p in self.positions:
            pygame.draw.rect(window, self.color, (p[0], p[1], 20, 20))

# Define the food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, WIDTH // 20 - 1) * 20, random.randint(0, HEIGHT // 20 - 1) * 20)

    def render(self):
        pygame.draw.rect(window, self.color, (self.position[0], self.position[1], 20, 20))

# Create instances of Snake and Food
snake = Snake()
food = Food()

# Set up the game clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, 1):
                snake.direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                snake.direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                snake.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                snake.direction = (1, 0)

    # Update snake
    snake.update()

    # Check if snake eats the food
    if snake.get_head_position() == food.position:
        snake.size += 1
        food.randomize_position()

    # Render the game
    window.fill(BLACK)
    snake.render()
    food.render()
    pygame.display.update()

    # Set the game speed
    clock.tick(10)

# Quit the game
pygame.quit()