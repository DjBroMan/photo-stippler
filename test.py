import pygame
from Point import Point

# Colors
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
YELLOW  = (255, 255, 0)
CYAN    = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE  = (255, 165, 0)
PURPLE  = (128, 0, 128)

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

# Clock
clock = pygame.time.Clock()

p = Point((50,50),radius= 5, color= BLUE)
t = Point((750,550),radius=50, color= WHITE)

p.setTarget(t)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    # update logic
    p.steer()
    p.update()

    # Draw
    screen.fill(BLACK)
    # draw logic

    t.show(screen)
    p.show(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()