import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Car Game")

# Load sounds
crash_sound = pygame.mixer.Sound("crash.mp3")
power_up_collect_sound = pygame.mixer.Sound("power.mp3")
pygame.mixer.music.load("back.mp3")
pygame.mixer.music.play(-1)  # Play background music indefinitely

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Car parameters
car_width, car_height = 50, 100
car_x = (WIDTH - car_width) // 2
car_y = HEIGHT - car_height - 20
car_speed = 5

# Track parameters
track_color = GREEN
track_rect = pygame.Rect(100, 50, WIDTH - 200, HEIGHT - 100)

# Opponent car parameters
opponent_width, opponent_height = 50, 100
opponent_speed = 3
opponent_cars = []

# Power-up parameters
power_up_width, power_up_height = 30, 30
power_up_speed = 3
power_ups = []

# Scoring
score = 0
font = pygame.font.SysFont(None, 40)
score_multiplier = 1

# Load images
background_image = pygame.image.load("back.jpeg")  # Replace "back.jpeg" with your image file
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
car_image = pygame.image.load("car.png")  # Replace "car.png" with the file name of your car image
car_image = pygame.transform.scale(car_image, (car_width, car_height))  # Scale the car image to match the car dimensions
opponent_image = pygame.image.load("enemy.png")  # Replace "enemy.png" with the file name of your enemy image
opponent_image = pygame.transform.scale(opponent_image, (opponent_width, opponent_height))  # Scale the enemy image to match the opponent car dimensions

# Game over variables
game_over = False
game_over_font = pygame.font.SysFont(None, 72)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Level parameters
level = 1
max_level = 5
opponent_speeds = [3, 4, 5, 6, 7]  # Speeds for each level

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Draw track first
        pygame.draw.rect(screen, track_color, track_rect)
        screen.blit(background_image, (0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x -= car_speed
        if keys[pygame.K_RIGHT]:
            car_x += car_speed

        car_x = max(track_rect.left, min(track_rect.right - car_width, car_x))

        # Draw the player's car
        screen.blit(car_image, (car_x, car_y))

        # Increase level based on score
        if score > 0 and score % 10 == 0 and level < max_level:
            level += 1
            draw_text(f"Level Upgraded to {level}", font, BLACK, WIDTH // 2, HEIGHT // 2)

        # Generate opponent cars with varying speeds based on level
        if len(opponent_cars) < 3:
            if random.randint(0, 100) < 5:
                x = random.randint(track_rect.left, track_rect.right - opponent_width)
                y = random.randint(-200, -100)
                opponent_cars.append(pygame.Rect(x, y, opponent_width, opponent_height))

                # Randomly select opponent speed within a range based on level
                opponent_speed = random.randint(opponent_speeds[level - 1] - 1, opponent_speeds[level - 1] + 1)

        for opponent_car in opponent_cars:
            opponent_car.y += opponent_speed
            # Draw the opponent car image
            screen.blit(opponent_image, (opponent_car.x, opponent_car.y))

            if opponent_car.colliderect((car_x, car_y, car_width, car_height)):
                game_over = True
                crash_sound.play()
                pygame.mixer.music.stop()

            if opponent_car.top > HEIGHT:
                opponent_cars.remove(opponent_car)
                score += 1 * score_multiplier

        # Generate power-ups
        if random.randint(0, 1000) < 5:
            power_up_x = random.randint(track_rect.left, track_rect.right - power_up_width)
            power_up_y = random.randint(-200, -100)
            power_up = pygame.Rect(power_up_x, power_up_y, power_up_width, power_up_height)
            power_ups.append(power_up)

        # Move and draw power-ups
        for power_up in power_ups:
            power_up.y += power_up_speed
            pygame.draw.rect(screen, YELLOW, power_up)

            # Check collision with player
            if power_up.colliderect((car_x, car_y, 50, 50)):
                power_ups.remove(power_up)
                car_speed += 2  # Increase car speed on power-up pickup
                power_up_collect_sound.play()
                score_multiplier = 2  # Activate score multiplier on power-up pickup

        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))
        level_text = font.render("Level: " + str(level), True, WHITE)
        screen.blit(level_text, (10, 40))

    else:
        draw_text("Game Over", game_over_font, RED, WIDTH // 2, HEIGHT // 2)
        draw_text("Press R to Restart", font, BLACK, WIDTH // 2, HEIGHT // 2 + 100)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            score = 0
            car_x = (WIDTH - car_width) // 2
            opponent_cars.clear()
            pygame.mixer.music.play(-1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
