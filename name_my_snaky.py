import pygame
import pygame_gui
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
WHITE = (255, 255, 255)

# Set up font
pygame.font.init()
myfont = pygame.font.Font(None, 30)

# Define the snake class
class Snake:
    def __init__(self, name=None):
        self.size = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.color = BLUE
        self.name = list(name.upper() if name else "")
        self.name_revealed = []

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * 20)) % WIDTH), (cur[1] + (y * 20)) % HEIGHT)

        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.size:
                self.positions.pop()
        return True

    def reset(self):
        self.size = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.name_revealed = []

    def render(self):
        for index, p in enumerate(self.positions):
            pygame.draw.rect(window, self.color, (p[0], p[1], 20, 20))

            # Print the name on the snake
            if index < len(self.name_revealed):
                name_surface = myfont.render(self.name_revealed[index], False, WHITE)
                window.blit(name_surface, (p[0], p[1]))

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

def start_screen():
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    hello_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 120), (540, 50)),
                                              text='Welcome to Snakey! Would you like to name your snake?',
                                              manager=manager)

    yes_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((210, 200), (100, 50)),
                                              text='YES',
                                              manager=manager)

    skip_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320, 200), (100, 50)),
                                               text='SKIP',
                                               manager=manager)

    text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((210, 260), (210, 50)),
                                                     manager=manager)
    text_entry.hide()

    clock = pygame.time.Clock()
    is_running = True
    snake_name = None

    while is_running:
        time_delta = clock.tick(30) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == yes_button:
                        yes_button.hide()
                        skip_button.hide()
                        hello_label.hide()
                        text_entry.show()
                    if event.ui_element == skip_button:
                        return None
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    snake_name = text_entry.get_text()
                    is_running = False

            manager.process_events(event)

        manager.update(time_delta)

        window.fill(BLACK)
        manager.draw_ui(window)

        pygame.display.update()

    return snake_name

snake_name = start_screen()
snake = Snake(snake_name)
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
    if not snake.update():
        snake_name = start_screen()
        snake = Snake(snake_name)
        food = Food()

    # Check if snake eats the food
    if snake.get_head_position() == food.position:
        snake.size += 1
        if snake.name:
            snake.name_revealed.append(snake.name.pop(0))
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