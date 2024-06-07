# Street Fighter Game
# By: Adrian Adewunmi
# Date: 04/09/2022
# Version: 1.0
# Description: This is the main file for the Street Fighter Game.
#             It contains the main game loop and the main game functions.
#             It also contains the main menu and the game over screen.
#             It also contains the high score screen.
#             It also contains the pause screen.
#             It also contains the game over screen.
# Adapted from:
# Coding With Ross
# Youtube URL: https://www.youtube.com/watch?v=s5bd9KMSSW4
# GitHub URL: https://github.com/russs123/brawler_tut
import pygame
from pygame import mixer
from fighter import Fighter
from controller import PlayerController
from ai import AIController

# Initialise Pygame
pygame.init()

# Initialise Mixer
mixer.init()

# Create Game Window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street Fighter!")

# Set Framerate
clock = pygame.time.Clock()
FPS = 60

# Define Colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Define Game Intro Count Variables
intro_count = 3
last_count_update = pygame.time.get_ticks()

# Define Variables For Player Game Score
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Define Fighter Sprite Sheet Image Variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

# Load warrior sword and wizard staff sound effect
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.75)
staff_fx = pygame.mixer.Sound("assets/audio/magic.wav")
staff_fx.set_volume(0.75)

# Load Background Image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# Load Warrior Sprite sheets Of Images
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
# Load Wizard Sprite sheets Of Images
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Load Victory Image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Define number of steps in each animation for Warrior and Wizard Player
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Define Fonts
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)


# Function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Function For Drawing Background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


# Function For Drawing Fighter Health Bar
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 5, y - 5, 410, 40))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, (400 * ratio), 30))
    
# Create controller instances
controller_1 = PlayerController(1)
controller_2 = AIController(2)

# Create Two Instances Of Fighter
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, staff_fx)

# Create Game Loop
run = True
game_paused = False

while run:
    clock.tick(FPS)

    # Draw Background
    draw_bg()

    # Show Player Stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)
    
    # Create the game_state dictionary
    game_state = {
        "fighter_1": {
            "position": fighter_1.rect,
            "alive": fighter_1.alive,
            "health": fighter_1.health
        },
        "fighter_2": {
            "position": fighter_2.rect,
            "alive": fighter_2.alive,
            "health": fighter_2.health
        },
        "round_over": round_over
    }
    
    # Get state changes from controllers
    state_changes_1 = controller_1.get_action(game_state)
    state_changes_2 = controller_2.get_action(game_state)    

    # Update Countdown
    if intro_count <= 0:
        # Move Fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_2, round_over, state_changes_1)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_1, round_over, state_changes_2)
    else:
        #display level difficulty
        draw_text(f"Level {controller_2.difficulty}", 
                  count_font, 
                  WHITE, 
                  SCREEN_WIDTH / 2-100, 
                  SCREEN_HEIGHT / 3-100)
        # display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # Update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # Update Fighters
    fighter_1.update()
    fighter_2.update()

    # Draw Fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Check for player defeat
    if not round_over:
        if not fighter_1.alive:
            score[1] += 1
            round_over = True
            controller_1.difficulty += 1
            round_over_time = pygame.time.get_ticks()
        elif not fighter_2.alive:
            score[0] += 1
            round_over = True
            controller_2.difficulty += 1
            round_over_time = pygame.time.get_ticks()
    else:
        # Display "Victory" Image
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            # Create Two Instances Of Fighter
            fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, staff_fx)

    # Implement Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    # Update Display
    pygame.display.update()

# Exit PyGame
pygame.quit()
