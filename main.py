import pygame
from pygame.locals import *
import time
import random

SIZE = 40
ORIGINNAL_LENGTH = 3

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3
    
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        # Coordinates of apple are multiples of SIZE so that apple and snake 
        # can align so they can meet
        self.x = random.randint(0, 24) * SIZE # 24 is max position apple should appear on the width of screen (1000 pixel/40 (constant size)
        self.y = random.randint(0, 19) * SIZE # 19 is max position apple should appear on the height of screen (800 pixel/40 (constant size)


class Snake:
    def __init__(self, parent_sceen, length):
        self.length = length
        self.parent_screen = parent_sceen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):
        for i in range(self.length - 1, 0, -1): # Make all blocks behind head move to the position of the block right before it
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up": # Make head (first block) move according to the direction
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE

        self.draw()
    
    def move_up(self):
        self.direction = "up"
    
    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Have fun playing my Snake Game!")
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface, ORIGINNAL_LENGTH)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
            
        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/background_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        background = pygame.image.load("resources/background.jpg")
        self.surface.blit(background, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding with itself
        for i in range(4, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game over"
        
        # Snake hitting walls
        if self.snake.x[0] < 0 or self.snake.x[0] > 1000 or self.snake.y[0] < 0 or self.snake.y[0] > 800:
            self.play_sound("crash")
            raise "Game over"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length - ORIGINNAL_LENGTH}.", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"To play again, press Enter. To exit, press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - ORIGINNAL_LENGTH}", True, (255, 255, 255))
        self.surface.blit(score, (820, 20))

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP and self.snake.direction != "down":
                            self.snake.move_up()
                        if event.key == K_DOWN and self.snake.direction != "up":
                            self.snake.move_down()
                        if event.key == K_LEFT and self.snake.direction != "right":
                            self.snake.move_left()
                        if event.key == K_RIGHT and self.snake.direction != "left":
                            self.snake.move_right()

                elif event.type == pygame.QUIT:
                    running = False

            try:
                if not pause:
                    self.play()  
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)
    
if __name__ == "__main__":
    game = Game()
    game.run()