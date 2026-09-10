from Point import Point
import pygame
import random
from typing import List, Tuple

# ---------------- CONSTANTS ----------------
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLUE: Tuple[int, int, int] = (0, 0, 255)


def main() -> None:
    """
    Demo: Multiple particles smoothly steering toward the mouse cursor.
    """

    pygame.init()

    # -------- SCREEN SETUP --------
    screen: pygame.Surface = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Steering - Mouse Follow")

    clock: pygame.time.Clock = pygame.time.Clock()

    w: int = screen.get_width()
    h: int = screen.get_height()

    # -------- CREATE POINTS --------
    points: List[Point] = []

    for _ in range(100):
        # Random starting position
        x: int = random.randint(0, w)
        y: int = random.randint(0, h)

        p: Point = Point((x, y))  # ✅ FIXED (no tuple target)

        # Random initial velocity
        vx: float = random.uniform(-3, 3)
        vy: float = random.uniform(-3, 3)
        p.setVelocity(vx, vy)

        # Random bright color
        color: Tuple[int, int, int] = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
        )
        p.color = color
        p.curr_color = color  # keep render color synced

        points.append(p)

    # -------- SHARED MOUSE TARGET (optimized) --------
    mouse_target: Point = Point((0, 0))

    # -------- MAIN LOOP --------
    running: bool = True
    while running:
        clock.tick(60)
        screen.fill((0, 0, 0))

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # -------- UPDATE MOUSE TARGET --------
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()
        mouse_target.setPos(*mouse_pos)

        # -------- UPDATE + DRAW --------
        for p in points:
            # Set same shared target for all particles
            p.setTarget(mouse_target)

            # Apply steering
            p.steer()

            # Update motion + interpolation
            p.update()

            # Render
            p.show(screen)

        # Draw mouse indicator
        pygame.draw.circle(
            screen,
            BLUE,
            mouse_pos,
            6
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()