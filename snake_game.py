import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 600

# Grid size
GRID_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling speed
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 25)


class SnakeGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.snake = [(100, 100)]
        self.direction = "RIGHT"
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

    def generate_food(self):
        while True:
            x = random.randrange(0, WIDTH, GRID_SIZE)
            y = random.randrange(0, HEIGHT, GRID_SIZE)

            if (x, y) not in self.snake:
                return (x, y)

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == "UP":
            new_head = (head_x, head_y - GRID_SIZE)

        elif self.direction == "DOWN":
            new_head = (head_x, head_y + GRID_SIZE)

        elif self.direction == "LEFT":
            new_head = (head_x - GRID_SIZE, head_y)

        elif self.direction == "RIGHT":
            new_head = (head_x + GRID_SIZE, head_y)

        # Wall collision
        if (
            new_head[0] < 0 or
            new_head[0] >= WIDTH or
            new_head[1] < 0 or
            new_head[1] >= HEIGHT
        ):
            self.game_over = True
            return

        # Self collision
        if new_head in self.snake:
            self.game_over = True
            return

        # Move snake
        self.snake.insert(0, new_head)

        # Food collision
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def draw_elements(self):
        screen.fill(BLACK)

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(
                screen,
                GREEN,
                (segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            )

        # Draw food
        pygame.draw.rect(
            screen,
            RED,
            (self.food[0], self.food[1], GRID_SIZE, GRID_SIZE)
        )

        # Draw score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()

    def show_game_over(self):
        screen.fill(BLACK)

        game_over_text = font.render(
            f"Game Over! Score: {self.score}",
            True,
            WHITE
        )

        restart_text = font.render(
            "Press R to Restart or Q to Quit",
            True,
            WHITE
        )

        screen.blit(game_over_text, (140, 250))
        screen.blit(restart_text, (90, 300))

        pygame.display.update()

    def run(self):
        running = True

        while running:
            clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.direction = "UP"

                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"

                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"

                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"

                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset_game()

                        elif event.key == pygame.K_q:
                            running = False

            if not self.game_over:
                self.move_snake()
                self.draw_elements()
            else:
                self.show_game_over()

        pygame.quit()


# Run game
game = SnakeGame()
game.run()