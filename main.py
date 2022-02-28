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


clock = pygame.time.Clock()

block_size = 20
FPS = 30

font = pygame.font.SysFont(None, 25)

def snake(block_size, snake_list):
    for XnY in snake_list:
        pygame.draw.rect(game_display, green, [XnY[0],XnY[1],block_size,block_size])

def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color)
    game_display.blit(screen_text, [display_width/2, display_height/2])


def gameLoop():
    game_exit = False
    game_over = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 0
    lead_y_change = 0

    snake_list = []
    snake_length = 1

    randAppleX = round(random.randrange(0, display_width-block_size))#/10.0)*10.0
    randAppleY = round(random.randrange(0, display_height-block_size))#/10.0)*10.0

    while not game_exit:
        while game_over == True:
            game_display.fill(white)
            message_to_screen("Game over, press C to play again or Q to quit", red)
            pygame.display.update()

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
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size    
                    lead_x_change = 0

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            game_over = True
        

        lead_x += lead_x_change
        lead_y += lead_y_change

        game_display.fill(white)

        apple_thickness = 30
        pygame.draw.rect(game_display, red, [randAppleX, randAppleY, apple_thickness, apple_thickness])

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

        pygame.display.update()

        # if lead_x >=randAppleX and lead_x <= randAppleX + apple_thickness:
        #     if lead_y >=randAppleY and lead_y <= randAppleY + apple_thickness:
        #         randAppleX = round(random.randrange(0, display_width-block_size)/10.0)*10.0
        #         randAppleY = round(random.randrange(0, display_height-block_size)/10.0)*10.0
        #         snake_length += 1

        if lead_x > randAppleX and lead_x < randAppleX + apple_thickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + apple_thickness:
            if lead_y > randAppleY and lead_y < randAppleY + apple_thickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + apple_thickness:
                print("xyyy")

        clock.tick(FPS)

    pygame.quit()
    quit()

gameLoop()