import pygame
import random
import os

pygame.mixer.init()

pygame.init()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 128)

# window
screen_width = 900
screen_height = 600
gamewindow = pygame.display.set_mode((screen_width, screen_height))

# background
bgimg_midle= pygame.image.load("green.jpg")
bgimg_midle = pygame.transform.scale(bgimg_midle, (screen_width, screen_height)).convert_alpha()

bgimg_end = pygame.image.load("end_image.jpg")
bgimg_end = pygame.transform.scale(bgimg_end, (screen_width, screen_height)).convert_alpha()

bgimg_front = pygame.image.load("front_image.jpg")
bgimg_front = pygame.transform.scale(bgimg_front, (screen_width, screen_height)).convert_alpha()

# Game title
pygame.display.set_caption("SnakesWithHappy")
pygame.display.update()

clock = pygame.time.Clock()
font1 = pygame.font.SysFont(None, 40, )
font2 = pygame.font.SysFont(None, 60, )
font3 = pygame.font.SysFont(None, 40, )


def text_screen(text, color, x, y):
    screen_text = font1.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])


def text_screen_heading(text, color, x, y):
    screen_text = font2.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])


def text_screen_logo(text, color, x, y):
    screen_text = font3.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])


def plot_snake(gamewindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.circle(gamewindow, color, (x, y), snake_size)


# welcome_game
def Welcome():
    exit_game = False

    while not exit_game:
        gamewindow.blit(bgimg_front, (0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("back_music.mp3")
                    pygame.mixer.music.play()
                    game_loop()

        pygame.display.update()
        clock.tick(30)


# Game Loop

def game_loop():
    # game spec:
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 50
    snake_size = 11
    init_variable = 7
    food_size = 11
    fps = 30
    velocity_x = 0
    velocity_y = 0
    score = 0

    # check hiscore file
    if (not os.path.exists("hiscore")):
        with open("hiscore", "w") as f:
            f.write("0")

    with open("hiscore", "r") as f:
        hiscore = f.read()

    snake_list = []
    snake_lenght = 3

    food_x = random.randint(20, screen_width // 2)
    food_y = random.randint(20, screen_height // 2)

    while not exit_game:

        if game_over:
            with open("hiscore", "w") as f:
                f.write(str(hiscore))

            gamewindow.blit(bgimg_end, (0, 0))
            text_screen_logo("Score: " + str(score), white, 360, 300)
            text_screen_logo("High Score: " + str(hiscore), white, 320, 330)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load("back_music.mp3")
                        pygame.mixer.music.play()
                        game_loop()



        else:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_variable
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_variable
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_variable
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_variable
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 10

                    if event.key == pygame.K_w:
                        hiscore = 0



            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 4\
                    and abs(snake_y - food_y) < 4:
                score += 10
                snake_lenght += 3

                food_x = random.randint(20, screen_width // 2)
                food_y = random.randint(20, screen_height // 2)
            if score > int(hiscore):
                hiscore = score

            #gamewindow.fill(white)
            gamewindow.blit(bgimg_midle, (0, 0))

            pygame.draw.circle(gamewindow, red, (food_x, food_y), food_size)
            text_screen("Score: " + str(score), white, 15, 5)
            text_screen(" High Score: " + str(hiscore), white, 650, 5)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_lenght:
                del snake_list[0]

            if head in snake_list[:-3]:
                game_over = True
                pygame.mixer.music.load("back_music.mp3")
                pygame.mixer.music.stop()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("back_music.mp3")
                pygame.mixer.music.stop()

            plot_snake(gamewindow, black, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


Welcome()
