import pygame
import sys
import random
from collections import deque
import time


def create_initial_window():
    screen.fill((1, 1, 1))
    font = pygame.font.Font(None, 36)
    text = font.render("Choose your level:", True, (255, 255, 255))
    screen.blit(text, (200, 100))

    easy_button = pygame.Rect(150, 200, 100, 50)
    medium_button = pygame.Rect(300, 200, 125, 50)
    hard_button = pygame.Rect(450, 200, 100, 50)

    pygame.draw.rect(screen, (0, 255, 0), easy_button)
    pygame.draw.rect(screen, (255, 255, 0), medium_button)
    pygame.draw.rect(screen, (255, 0, 0), hard_button)

    easy_text = font.render("Easy", True, (0, 0, 0))
    medium_text = font.render("Medium", True, (0, 0, 0))
    hard_text = font.render("Hard", True, (0, 0, 0))

    screen.blit(easy_text, (170, 215))
    screen.blit(medium_text, (310, 215))
    screen.blit(hard_text, (470, 215))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if easy_button.collidepoint(x, y):
                    # print("easy")
                    return "easy"
                elif medium_button.collidepoint(x, y):
                    # print("medium")
                    return "medium"
                elif hard_button.collidepoint(x, y):
                    # print("hard")
                    return "hard"


def create_game_window(difficulty):
    def get_diff(difficulty):

        num_obstacles = 0
        if difficulty == "easy":
            num_obstacles = 20
        elif difficulty == "medium":
            num_obstacles = 40
        elif difficulty == "hard":
            num_obstacles = 60
        return num_obstacles

    def generate_obstacles(grid_size, num_obstacles):
        grid = [[0] * grid_size for _ in range(grid_size)]

        def is_valid(grid, x, y, n):
            if x >= n or y >= n or grid[x][y] == 1:
                return False
            else:
                return True

        def solve_it(grid, x, y, n, smat):
            if x == n - 1 and y == n - 1:
                smat[x][y] = 1
                return True
            if is_valid(grid, x, y, n):
                smat[x][y] = 1
                if solve_it(grid, x + 1, y, n, smat):
                    return True
                if solve_it(grid, x, y + 1, n, smat):
                    return True
                smat[x][y] = 0
                return False
            else:
                return False

        # print(x,y)
        def create_obstacles(grid, n_obs):

            grid_size = len(grid)
            obstacles = 0
            chances = 0
            smat_0 = [[0] * len(grid) for _ in range(len(grid))]
            while obstacles < n_obs and chances < 10000:
                x = random.randint(0, grid_size - 1)
                y = random.randint(0, grid_size - 1)
                if (x, y) != (0, 0) and (x, y) != (grid_size - 1, grid_size - 1) and grid[x][y] == 0:
                    grid[x][y] = 1
                    if solve_it(grid, 0, 0, grid_size, smat_0):
                        obstacles += 1
                    else:
                        grid[x][y] = 0
                chances += 1
            # obstacle_positions = [(x, y) for x in range(grid_size) for y in range(grid_size) if grid[x][y] == 1]
            obstacle_positions = []
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] == 1:
                        obstacle_positions.append([i, j])

            # print("Start")
            # for i in grid:
            #   print(i)
            # smat_1 = [[0] * len(grid) for _ in range(len(grid))]
            # print("-----------------------------------------")
            # solve_it(grid, 0, 0, len(grid), smat_1)
            # for i in smat_1:
            #   print(i)
            return obstacle_positions

        xx = create_obstacles(grid, num_obstacles)
        # print(xx)
        return xx

    def convert():
        grid_size = 14
        num_obstacles = get_diff(difficulty)
        obstacles = generate_obstacles(grid_size, num_obstacles)
        for i in range(len(obstacles)):
            obstacles[i] = list(obstacles[i])
        for i in range(len(obstacles)):
            for j in range(len(obstacles[i])):
                obstacles[i][j] = 50 * (obstacles[i][j] + 1)
        for i in range(len(obstacles)):
            temp = obstacles[i][0]
            obstacles[i][0] = obstacles[i][1]
            obstacles[i][1] = temp
        # print(obstacles)
        return obstacles

    def obstacle(screen):
        ball_color = (255, 0, 0)
        pygame.draw.circle(screen, ball_color, (x, y), radius)
        pygame.display.update()
        time.sleep(0.25)
        ball_color = (255, 255, 255)

    def victory_text(screen):
        screen.fill((2, 2, 2))

        title_drag_text = title_font.render("Congratulations!", True, (255, 255, 0))
        title_ball_text = title_font.render("You Won", True, (0, 0, 255))
        title_drag_text_rect = title_drag_text.get_rect()
        title_ball_text_rect = title_ball_text.get_rect()
        title_drag_text_rect.center = (750 / 2, 750 / 2)
        title_ball_text_rect.center = ((750 / 2) + 10, (850 / 2) + 10)
        screen.blit(title_drag_text, title_drag_text_rect)
        screen.blit(title_ball_text, title_ball_text_rect)

    def victory(screen):
        ball_color = (0, 255, 0)
        pygame.draw.circle(screen, ball_color, (x, y), radius)
        pygame.display.update()
        time.sleep(0.25)
        ball_color = (255, 255, 255)

    collision_points = convert()
    pygame.init()
    screen = pygame.display.set_mode((750, 750))
    pygame.display.set_caption("Drag Ball!")
    x = 50
    y = 50
    X1 = 50
    y1 = 50
    title_font = pygame.font.Font('freesansbold.ttf', 40)

    title_drag_text = title_font.render("Drag", True, (0, 255, 0))
    title_ball_text = title_font.render("Ball", True, (255, 255, 255))
    title_drag_text_rect = title_drag_text.get_rect()
    title_ball_text_rect = title_ball_text.get_rect()
    title_drag_text_rect.center = (screen.get_width() // 2 - 70, 30)
    title_ball_text_rect.center = (screen.get_width() // 2 + 70, 30)
    screen.blit(title_drag_text, title_drag_text_rect)
    screen.blit(title_ball_text, title_ball_text_rect)
    width = 40
    height = 60
    radius = 12
    vel = 50
    won = False
    run = True
    while run:
        pygame.time.delay(100)
        run = True

        while run:
            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()

            pygame.draw.line(screen, (255, 255, 255), (x, y), (x, y + 100), (5))
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and x < 700 and y % 50 == 0:
                x += vel
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and x > 50 and y % 50 == 0:
                x -= vel
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and y > 50 and x % 50 == 0:
                y -= vel
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and y < 700 and x % 50 == 0:
                y += vel
            screen.fill((2, 2, 2))
            # print("Points: ", (x, y))
            if won == False:
                title_drag_text = title_font.render("Drag", True, (0, 255, 0))
                title_ball_text = title_font.render("Ball", True, (255, 255, 255))
                title_drag_text_rect = title_drag_text.get_rect()
                title_ball_text_rect = title_ball_text.get_rect()
                title_drag_text_rect.center = (screen.get_width() // 2 - title_drag_text_rect.width // 2 - 10, 30)
                title_ball_text_rect.center = (screen.get_width() // 2 + title_ball_text_rect.width // 2 + 10, 30)
                screen.blit(title_drag_text, title_drag_text_rect)
                screen.blit(title_ball_text, title_ball_text_rect)
                pygame.draw.line(screen, (255, 255, 255), (X1, y1), (X1, y1 + 650), (1))
                pygame.draw.line(screen, (255, 0, 0), (X1 + 50, y1), (X1 + 50, y1 + 650), (1))
                pygame.draw.line(screen, (255, 0, 255), (X1 + 100, y1), (X1 + 100, y1 + 650), (1))
                pygame.draw.line(screen, (0, 255, 255), (X1 + 150, y1), (X1 + 150, y1 + 650), (1))
                pygame.draw.line(screen, (255, 255, 0), (X1 + 200, y1), (X1 + 200, y1 + 650), (1))
                pygame.draw.line(screen, (0, 0, 255), (X1 + 250, y1), (X1 + 250, y1 + 650), (1))
                pygame.draw.line(screen, (0, 255, 0), (X1 + 300, y1), (X1 + 300, y1 + 650), (1))
                pygame.draw.line(screen, (255, 128, 0), (X1 + 350, y1), (X1 + 350, y1 + 650), (1))
                pygame.draw.line(screen, (255, 153, 255), (X1 + 400, y1), (X1 + 400, y1 + 650), (1))
                pygame.draw.line(screen, (50, 205, 50), (X1 + 450, y1), (X1 + 450, y1 + 650), (1))
                pygame.draw.line(screen, (128, 0, 128), (X1 + 500, y1), (X1 + 500, y1 + 650), (1))
                pygame.draw.line(screen, (166, 145, 115), (X1 + 550, y1), (X1 + 550, y1 + 650), (1))
                pygame.draw.line(screen, (199, 176, 118), (X1 + 600, y1), (X1 + 600, y1 + 650), (1))
                pygame.draw.line(screen, (150, 128, 255), (X1 + 650, y1), (X1 + 650, y1 + 650), (1))
                pygame.draw.line(screen, (150, 128, 255), (X1, y1), (X1 + 650, y1), (1))
                pygame.draw.line(screen, (199, 176, 118), (X1, y1 + 50), (X1 + 650, y1 + 50), (1))
                pygame.draw.line(screen, (166, 145, 115), (X1, y1 + 100), (X1 + 650, y1 + 100), (1))
                pygame.draw.line(screen, (128, 0, 128), (X1, y1 + 150), (X1 + 650, y1 + 150), (1))
                pygame.draw.line(screen, (50, 205, 50), (X1, y1 + 200), (X1 + 650, y1 + 200), (1))
                pygame.draw.line(screen, (255, 153, 255), (X1, y1 + 250), (X1 + 650, y1 + 250), (1))
                pygame.draw.line(screen, (255, 128, 0), (X1, y1 + 300), (X1 + 650, y1 + 300), (1))
                pygame.draw.line(screen, (0, 255, 0), (X1, y1 + 350), (X1 + 650, y1 + 350), (1))
                pygame.draw.line(screen, (0, 0, 255), (X1, y1 + 400), (X1 + 650, y1 + 400), (1))
                pygame.draw.line(screen, (255, 255, 0), (X1, y1 + 450), (X1 + 650, y1 + 450), (1))
                pygame.draw.line(screen, (0, 255, 255), (X1, y1 + 500), (X1 + 650, y1 + 500), (1))
                pygame.draw.line(screen, (255, 0, 255), (X1, y1 + 550), (X1 + 650, y1 + 550), (1))
                pygame.draw.line(screen, (255, 0, 0), (X1, y1 + 600), (X1 + 650, y1 + 600), (1))
                pygame.draw.line(screen, (255, 255, 255), (X1, y1 + 650), (X1 + 650, y1 + 650), (1))
                pygame.draw.circle(screen, (255, 255, 255), (x, y), (radius), (radius))

                if [x, y] in collision_points:
                    obstacle(screen)
                    x = 50
                    y = 50
                if [x, y] == [700, 700]:
                    won = True
                    victory(screen)
            else:
                victory_text(screen)

            pygame.display.update()
pygame.init()
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Choose Level")
while True:
    difficulty = create_initial_window()
    create_game_window(difficulty)

pygame.quit()
