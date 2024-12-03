import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jetpack Joyride")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
player_width, player_height = 50, 50
player_x, player_y = 100, HEIGHT // 2
player_speed = 5
player_gravity = 0.5
player_velocity = 0

# Obstacle settings
obstacle_width, obstacle_height = 50, 200
obstacle_gap = 200
obstacle_speed = 5
obstacle_timer = 1500  # Milliseconds
last_obstacle_time = pygame.time.get_ticks()

# Scoring
score = 0
font = pygame.font.Font(None, 36)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Obstacles list
obstacles = []

# Game loop control
running = True

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height))

def draw_obstacles(obstacles_list):
    for obstacle in obstacles_list:
        pygame.draw.rect(screen, RED, obstacle)

def check_collision(player_rect, obstacles_list):
    for obstacle in obstacles_list:
        if player_rect.colliderect(obstacle):
            return True
    return False

while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:  # Jetpack is active
        player_velocity = -8

    # Apply gravity
    player_velocity += player_gravity
    player_y += player_velocity

    # Boundary check
    if player_y < 0:
        player_y = 0
    if player_y > HEIGHT - player_height:
        player_y = HEIGHT - player_height

    # Create new obstacles
    current_time = pygame.time.get_ticks()
    if current_time - last_obstacle_time > obstacle_timer:
        obstacle_y = random.randint(100, HEIGHT - obstacle_gap - 100)
        top_obstacle = pygame.Rect(WIDTH, 0, obstacle_width, obstacle_y)
        bottom_obstacle = pygame.Rect(WIDTH, obstacle_y + obstacle_gap, obstacle_width, HEIGHT - obstacle_y - obstacle_gap)
        obstacles.append(top_obstacle)
        obstacles.append(bottom_obstacle)
        last_obstacle_time = current_time

    # Move obstacles
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed

    # Remove off-screen obstacles
    obstacles = [obs for obs in obstacles if obs.x > -obstacle_width]

    # Collision detection
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    if check_collision(player_rect, obstacles):
        print("Game Over!")
        running = False

    # Scoring
    for obstacle in obstacles:
        if obstacle.x + obstacle_width == player_x:
            score += 1

    # Draw player and obstacles
    draw_player(player_x, player_y)
    draw_obstacles(obstacles)

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Maintain frame rate
    clock.tick(FPS)

pygame.quit()
