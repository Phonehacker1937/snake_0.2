# Snake Game Coursework Report

## Introduction

### What is your application?
The Snake game is a classic arcade game where the player controls a snake to collect food, which increases the snake's length. The objective is to grow the snake as long as possible without colliding with the walls or itself.

### How to run the program?
1. Ensure Python is Installed: Make sure you have Python installed on your system.
2. Install Pygame: Pygame is a set of Python modules designed for writing video games. You can install it using pip, the Python package installer. Open a command prompt or terminal and run the following command:
```sh
pip install pygame
```
3. Download the Snake Game Files: Download the Python script and any necessary assets for the Snake game. Place them in a directory of your choice on your computer.
4. Navigate to the Directory: Use the command prompt or terminal to navigate to the directory where you placed the Snake game files.
5. Run the Program

### How to use the program?
1. Use the arrow keys to control the direction of the snake.
2. The snake will wrap around the screen when it hits the boundary.
3. Collect food to grow the snake and increase your score.
4. Avoid running into the snake’s own body, which will end the game.
# Body/Analysis
## Implementation of Functional Requirements
### Object-Oriented Programming Pillars


#### 1. Encapsulation:

The Snake, Food, and Game classes encapsulate related attributes and methods. This hides the internal workings and only exposes necessary interfaces.
```sh
class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = pygame.K_RIGHT  
```
#### 2. Inheritance:

Not explicitly shown in the current implementation but could be demonstrated by creating specialized food types or snake types through subclassing.
```sh
class SpecialFood(Food):
    def __init__(self, x, y, bonus_points):
        super().__init__(x, y)
        self.bonus_points = bonus_points
```
#### 3. Polymorphism:

The use of polymorphism can be seen in the handling of different events and sounds for different game actions (e.g., eating food, game over).
```sh
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = FoodFactory.create_food()
```
### Design Patterns
#### 1. Singleton Pattern:

Ensures there is only one instance of the Game class managing the game state.
```sh
class SingletonMeta(type):
    _instance = None
    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
```
#### 2. Factory Method Pattern:

Used to create food objects, encapsulating the instantiation logic.
```sh
class FoodFactory:
    @staticmethod
    def create_food():
        return Food(random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
```
## Unit Tests

Implemented using the unittest framework to cover core functionalities such as snake movement, collision detection, and direction change prevention.
python
```sh
class TestSnakeGame(unittest.TestCase):
    def test_snake_initialization(self):
        snake = Snake()
        self.assertEqual(len(snake.body), 3)
    ...
if __name__ == '__main__':
    unittest.main(exit=False)
```
# Results and Summary
## Results
- Successfully implemented a snake game with sound effects for eating food and game over.
- Incorporated object-oriented principles and design patterns effectively.
- Ensured code quality and correctness through unit testing.
- Implemented boundary wrapping and direction change prevention.

## Challenges Faced
- Handling edge cases in snake movement and collision detection.
- Ensuring smooth integration of sound effects.
- Implementing effective unit tests to cover various game scenarios.

## Conclusions
- The snake game implementation demonstrates the effective use of OOP principles and design patterns.
- The program is extensible and can be expanded with additional features such as special foods, multiple levels, or enhanced graphics.
- The project achieved a functional and entertaining snake game that follows good coding practices.

## Future Prospects
- Adding a database to store high scores and player profiles with date and time of achievement.
- Implementing more complex game mechanics such as obstacles and power-ups.
- Enhancing the game's user interface and graphics for a more engaging user experience.
