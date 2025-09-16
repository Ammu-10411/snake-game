import pygame
import random
import sys


pygame.init()
WIDTH, HEIGHT = 600, 400
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("King Cobra - NeoSnake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 22)

BLACK = (0, 0, 0)
GREEN = (0, 200, 80)
DARKGREEN = (0, 150, 60)
RED = (220, 60, 60)
WHITE = (240, 240, 240)

class Snake:
    def __init__(self):
        self.body = [(WIDTH // (2 * CELL), HEIGHT // (2 * CELL))]
        self.dir = (1, 0) 
        self.grow = False

    def head(self):
        return self.body[0]

    def move(self):
        hx, hy = self.head()
        dx, dy = self.dir
        new_head = (hx + dx, hy + dy)

    
        if not (0 <= new_head[0] < WIDTH // CELL and 0 <= new_head[1] < HEIGHT // CELL):
            return False
        
        if new_head in self.body:
            return False

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True

    def change_dir(self, d):
        opposite = (-self.dir[0], -self.dir[1])
        if d != opposite:
            self.dir = d

def random_food(snake_body):
    cols = WIDTH // CELL
    rows = HEIGHT // CELL
    while True:
        pos = (random.randint(0, cols - 1), random.randint(0, rows - 1))
        if pos not in snake_body:
            return pos


def draw_snake(snake):
    for i, (x, y) in enumerate(snake.body):
        color = GREEN if i == 0 else DARKGREEN
        rect = pygame.Rect(x * CELL, y * CELL, CELL - 2, CELL - 2)
        pygame.draw.rect(screen, color, rect, border_radius=6)

def draw_food(pos):
    rect = pygame.Rect(pos[0] * CELL, pos[1] * CELL, CELL - 2, CELL - 2)
    pygame.draw.rect(screen, RED, rect, border_radius=6)

def draw_score(score):
    txt = font.render(f"Score: {score}", True, WHITE)
    screen.blit(txt, (10, 10))

def game_loop():
    snake = Snake()
    food = random_food(snake.body)
    score = 0

    while True:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_UP, pygame.K_w):
                    snake.change_dir((0, -1))
                elif e.key in (pygame.K_DOWN, pygame.K_s):
                    snake.change_dir((0, 1))
                elif e.key in (pygame.K_LEFT, pygame.K_a):
                    snake.change_dir((-1, 0))
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    snake.change_dir((1, 0))
                elif e.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit(); sys.exit()


        alive = snake.move()
        if not alive:
            break

        
        if snake.head() == food:
            snake.grow = True
            score += 2
            food = random_food(snake.body)

        
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        draw_score(score)
        pygame.display.flip()
        clock.tick(5 + score // 1)  

    
    screen.fill(BLACK)
    over = font.render("GAME OVER - Press R to Restart or Q to Quit", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return game_loop()
                elif e.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit(); sys.exit()

if __name__ == "__main__":
    game_loop()
