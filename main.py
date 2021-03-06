import os
import pygame
import random

# Opens window in second monitor
x = 1920
y = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0, 155, 0)

display_width = 800
display_height = 600

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')

icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

img = pygame.image.load('snakehead.png')
apple_img = pygame.image.load('apple.png')

clock = pygame.time.Clock()

apple_thickness = 30
block_size = 20
FPS = 15

direction = "right"

small_font = pygame.font.SysFont("comicsansms", 25)
med_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("comicsansms", 80)

def pause():
    paused = True
    message_to_screen("Paused", black, -100, size="large")
    message_to_screen("Press C to continue or Q to quit", black)

    pygame.display.update()
    clock.tick(5)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit() 

        # game_display.fill(white)
        

def score(score):
    text = small_font.render('Score: ' + str(score), True, black)
    game_display.blit(text, [0,0])

def rand_apple_gen():
    randAppleX = round(random.randrange(0, display_width-apple_thickness)/10.0)*10.0
    randAppleY = round(random.randrange(0, display_height-apple_thickness)/10.0)*10.0

    return randAppleX, randAppleY

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        game_display.fill(white)
        message_to_screen("Welcome to Slither", green, -100, "large")
        message_to_screen("The objective of the game is to eat red apples", black, -30)
        message_to_screen("The more apples you eat the longer you get", black, 10)
        message_to_screen("If you run into yourself, or the edges, you die!", black, 50)
        message_to_screen("Press C to play, P to pause or Q to quit", black, 180)

        pygame.display.update()

def snake(block_size, snake_list):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)

    game_display.blit(head, (snake_list[-1][0], snake_list[-1][1]))

    for XnY in snake_list[:-1]:
        pygame.draw.rect(game_display, green, [XnY[0],XnY[1],block_size,block_size])

def text_objects(text, color, size):
    if size == "small":
        text_surface = small_font.render(text, True, color)
    elif size == "medium":
        text_surface = med_font.render(text, True, color)
    elif size == "large":
        text_surface = large_font.render(text, True, color)
            
    return text_surface, text_surface.get_rect()



def message_to_screen(msg, color, y_displace=0, size="small"):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2),  (display_height / 2) + y_displace
    game_display.blit(text_surf, text_rect)


def gameLoop():
    global direction

    direction = 'right'
    game_exit = False
    game_over = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 10
    lead_y_change = 0

    snake_list = []
    snake_length = 1

    randAppleX, randAppleY = rand_apple_gen()

    while not game_exit:
        if game_over:
            message_to_screen("Game over", red, -50, size="large")
            message_to_screen("Press C to play again or Q to quit", black, 50, size="medium")
            pygame.display.update()

        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.QUIT:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        gameLoop()
                elif event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size    
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            game_over = True
        

        lead_x += lead_x_change
        lead_y += lead_y_change

        game_display.fill(white)

        # pygame.draw.rect(game_display, red, [randAppleX, randAppleY, apple_thickness, apple_thickness])

        game_display.blit(apple_img, (randAppleX, randAppleY))

        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)
        snake(block_size, snake_list)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for each_segment in snake_list[:-1]:
            if each_segment == snake_head:
                game_over = True
        
        score(snake_length-1)

        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX + apple_thickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + apple_thickness:
            if lead_y > randAppleY and lead_y < randAppleY + apple_thickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + apple_thickness:
                randAppleX, randAppleY = rand_apple_gen()
                snake_length += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
gameLoop()