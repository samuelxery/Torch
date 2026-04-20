import pygame
import random
import sys

# Constants
BLOCK_SIZE = 20
SPEED = 15
# Colors
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class SnakeGame:
    def __init__(self, width=640, height=480):
        pygame.init()
        self.w = width
        self.h = height
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake - ML Ready')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 25)
        self.reset()

    def reset(self):
        self.direction = 'RIGHT'
        self.head = [self.w / 2, self.h / 2]
        # Snake body
        self.snake = [[self.head[0], self.head[1]],
                      [self.head[0] - BLOCK_SIZE, self.head[1]],
                      [self.head[0] - (2 * BLOCK_SIZE), self.head[1]]]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = [x, y]
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. Event Handling (Prevents the "Not Responding" freeze)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != 'RIGHT':
                    self.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and self.direction != 'LEFT':
                    self.direction = 'RIGHT'
                elif event.key == pygame.K_UP and self.direction != 'DOWN':
                    self.direction = 'UP'
                elif event.key == pygame.K_DOWN and self.direction != 'UP':
                    self.direction = 'DOWN'

        # 2. Move
        self._move(self.direction)
        self.snake.insert(0, list(self.head))

        # 3. Check Game Over
        if self._is_collision():
            return True, self.score

        # 4. Food Logic
        if self.head[0] == self.food[0] and self.head[1] == self.food[1]:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. Draw and Tick
        self._update_ui()
        self.clock.tick(SPEED)
        return False, self.score

    def _is_collision(self):
        # Boundaries
        if self.head[0] >= self.w or self.head[0] < 0 or self.head[1] >= self.h or self.head[1] < 0:
            return True
        # Self-collision
        if self.head in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        # Draw Snake
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(pt[0], pt[1], BLOCK_SIZE, BLOCK_SIZE))

        # Draw Food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))

        # Draw Score
        text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])

        pygame.display.flip()

    def _move(self, direction):
        if direction == 'RIGHT':
            self.head[0] += BLOCK_SIZE
        elif direction == 'LEFT':
            self.head[0] -= BLOCK_SIZE
        elif direction == 'DOWN':
            self.head[1] += BLOCK_SIZE
        elif direction == 'UP':
            self.head[1] -= BLOCK_SIZE


if __name__ == '__main__':
    game = SnakeGame()
    while True:
        game_over, score = game.play_step()
        if game_over:
            print(f'Final Score: {score}')
            game.reset()