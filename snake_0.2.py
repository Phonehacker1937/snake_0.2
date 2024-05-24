import pygame
import sys
import random
import os
import unittest

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# File Paths
BASE_DIR = os.path.dirname(__file__)
CLICK_SOUND_PATH = os.path.join(BASE_DIR, "Click_02.wav")
DEATH_SOUND_PATH = os.path.join(BASE_DIR, "Dramatic Horn Transition 02.wav")
SAVE_FILE_PATH = os.path.join(BASE_DIR, "highscore.txt")

# Observer Pattern
class Event:
    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def unregister(self, listener):
        self.listeners.remove(listener)

    def notify(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)


class Game(metaclass=SingletonMeta):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = FoodFactory.create_food()
        self.direction = pygame.K_RIGHT
        self.score = 0
        self.highscore = self.load_highscore()
        self.font = pygame.font.SysFont(None, 35)

        # Load sounds with error handling
        self.eat_sound = self.load_sound(CLICK_SOUND_PATH)
        self.death_sound = self.load_sound(DEATH_SOUND_PATH)

        # Events
        self.food_eaten_event = Event()
        self.game_over_event = Event()
        self.food_eaten_event.register(self.on_food_eaten)
        self.game_over_event.register(self.on_game_over)

    def load_sound(self, path):
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        else:
            print(f"Warning: Sound file '{path}' not found.")
            return None

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    # Prevent the snake from reversing
                    if not self.snake.is_opposite_direction(event.key):
                        self.direction = event.key

    def update(self):
        self.snake.move(self.direction)
        if self.snake.collides_with_food(self.food):
            self.food_eaten_event.notify()
        self.snake.wrap_around()
        if self.snake.collides_with_self():
            self.game_over_event.notify()

    def draw(self):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        highscore_text = self.font.render(f"High Score: {self.highscore}", True, WHITE)
        self.screen.blit(score_text, [10, 10])
        self.screen.blit(highscore_text, [10, 40])
        pygame.display.flip()

    def on_food_eaten(self):
        self.snake.grow()
        self.food = FoodFactory.create_food()
        self.score += 10
        if self.eat_sound:
            self.eat_sound.play()

    def on_game_over(self):
        if self.death_sound:
            self.death_sound.play()
        self.update_highscore()
        self.show_game_over_screen()
        pygame.quit()
        sys.exit()

    def show_game_over_screen(self):
        self.screen.fill(BLACK)
        game_over_text = self.font.render("Game Over!", True, RED)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        highscore_text = self.font.render(f"High Score: {self.highscore}", True, WHITE)
        restart_text = self.font.render("Press R to Restart or Q to Quit", True, WHITE)
        self.screen.blit(game_over_text, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4])
        self.screen.blit(score_text, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + 50])
        self.screen.blit(highscore_text, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + 100])
        self.screen.blit(restart_text, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + 150])
        pygame.display.flip()
        self.wait_for_restart()

    def wait_for_restart(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()  # Reset game
                        self.run()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def load_highscore(self):
        if os.path.exists(SAVE_FILE_PATH):
            with open(SAVE_FILE_PATH, 'r') as file:
                return int(file.read())
        return 0

    def update_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open(SAVE_FILE_PATH, 'w') as file:
                file.write(str(self.highscore))

class FoodFactory:
    @staticmethod
    def create_food():
        return Food(random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, CELL_SIZE, CELL_SIZE))

class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = pygame.K_RIGHT

    def move(self, direction):
        if self.is_opposite_direction(direction):
            direction = self.direction  # Ignore the move if it's a reverse direction
        head_x, head_y = self.body[0]
        if direction == pygame.K_UP:
            head_y -= CELL_SIZE
        elif direction == pygame.K_DOWN:
            head_y += CELL_SIZE
        elif direction == pygame.K_LEFT:
            head_x -= CELL_SIZE
        elif direction == pygame.K_RIGHT:
            head_x += CELL_SIZE
        self.body.insert(0, (head_x, head_y))
        self.body.pop()
        self.direction = direction  # Update the direction after a valid move

    def grow(self):
        self.body.append(self.body[-1])

    def collides_with_food(self, food):
        return self.body[0] == (food.x, food.y)

    def wrap_around(self):
        head_x, head_y = self.body[0]
        if head_x < 0:
            head_x = SCREEN_WIDTH - CELL_SIZE
        elif head_x >= SCREEN_WIDTH:
            head_x = 0
        elif head_y < 0:
            head_y = SCREEN_HEIGHT - CELL_SIZE
        elif head_y >= SCREEN_HEIGHT:
            head_y = 0
        self.body[0] = (head_x, head_y)

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

    def is_opposite_direction(self, new_direction):
        opposite_directions = {
            pygame.K_UP: pygame.K_DOWN,
            pygame.K_DOWN: pygame.K_UP,
            pygame.K_LEFT: pygame.K_RIGHT,
            pygame.K_RIGHT: pygame.K_LEFT
        }
        return opposite_directions.get(self.direction) == new_direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

# Unit Tests
class TestSnakeGame(unittest.TestCase):
    def test_snake_initialization(self):
        snake = Snake()
        self.assertEqual(len(snake.body), 3)
        self.assertEqual(snake.body[0], (100, 100))

    def test_snake_movement(self):
        snake = Snake()
        snake.move(pygame.K_RIGHT)
        self.assertEqual(snake.body[0], (120, 100))

    def test_snake_grow(self):
        snake = Snake()
        initial_length = len(snake.body)
        snake.grow()
        self.assertEqual(len(snake.body), initial_length + 1)

    def test_snake_collides_with_food(self):
        snake = Snake()
        food = Food(100, 100)
        self.assertTrue(snake.collides_with_food(food))

    def test_food_creation(self):
        food = FoodFactory.create_food()
        self.assertIsInstance(food, Food)

    def test_game_initialization(self):
        game = Game()
        self.assertIsNotNone(game.snake)
        self.assertIsNotNone(game.food)

    def test_snake_prevent_reverse_direction(self):
        snake = Snake()
        self.assertFalse(snake.is_opposite_direction(pygame.K_DOWN))  # Initially facing right, can't go left
        snake.move(pygame.K_UP)  # Move up
        self.assertTrue(snake.is_opposite_direction(pygame.K_DOWN))  # Now can't go down
        snake.move(pygame.K_LEFT)  # Move left
        self.assertTrue(snake.is_opposite_direction(pygame.K_RIGHT))  # Now can't go right
        snake.move(pygame.K_DOWN)  # Move down
        self.assertTrue(snake.is_opposite_direction(pygame.K_UP))  # Now can't go up

if __name__ == '__main__':
    game = Game()
    unittest.main(exit=False)
    game.run()
