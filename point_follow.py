from Point import Point
import pygame
import random
from typing import List, Tuple

WHITE: Tuple[int, int, int] = (255, 255, 255)


def main() -> None:
    """
    Demo: Points following other points (swarm / chain behavior).
    Each point is assigned another point as its target.
    """

    pygame.init()

    # -------- SCREEN SETUP --------
    screen: pygame.Surface = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Points Following Points")

    clock: pygame.time.Clock = pygame.time.Clock()

    w: int = screen.get_width()
    h: int = screen.get_height()

    # -------- CREATE POINTS --------
    points: List[Point] = []

    for _ in range(1000):
        x: int = random.randint(0, w)
        y: int = random.randint(0, h)

        # ✅ FIX: no tuple target
        p: Point = Point((x, y))

        # Random velocity
        p.setVelocity(
            random.uniform(-3, 3),
            random.uniform(-3, 3)
        )

        # Random color
        color: Tuple[int, int, int] = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
        )
        p.color = color
        p.curr_color = color

        points.append(p)

    # -------- ASSIGN TARGET POINTS --------
    shuffled: List[Point] = points[:]
    random.shuffle(shuffled)

    # Avoid self-target
    for i in range(len(points)):
        if points[i] == shuffled[i]:
            swap_with: int = (i + 1) % len(points)
            shuffled[i], shuffled[swap_with] = shuffled[swap_with], shuffled[i]

    # Assign actual Point objects as targets
    for i in range(len(points)):
        points[i].target_point = shuffled[i]

    # -------- MAIN LOOP --------
    running: bool = True
    while running:
        clock.tick(60)
        screen.fill((0, 0, 0))

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # -------- UPDATE + DRAW --------
        for p in points:
            # ✅ FIX: pass Point object, not coordinates
            p.setTarget(p.target_point)

            p.steer()
            p.update()
            p.show(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()