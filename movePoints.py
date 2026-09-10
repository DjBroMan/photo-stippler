from Point import Point
import random
import pygame
from typing import List, Tuple

# ---------------- CONSTANTS ----------------
WHITE: Tuple[int, int, int]   = (255, 255, 255)
BLACK: Tuple[int, int, int]   = (0, 0, 0)
RED: Tuple[int, int, int]     = (255, 0, 0)
GREEN: Tuple[int, int, int]   = (0, 255, 0)
BLUE: Tuple[int, int, int]    = (0, 0, 255)
YELLOW: Tuple[int, int, int]  = (255, 255, 0)
CYAN: Tuple[int, int, int]    = (0, 255, 255)
MAGENTA: Tuple[int, int, int] = (255, 0, 255)
ORANGE: Tuple[int, int, int]  = (255, 165, 0)
PURPLE: Tuple[int, int, int]  = (128, 0, 128)

PADDING: int = 50


# ---------------- GENERATE POINTS ----------------
def generate_points(WIDTH: int, HEIGHT: int) -> Tuple[List[Point], List[Point]]:
    """
    Generates random points and target points within screen bounds.

    Returns:
        points  -> initial moving particles
        targets -> destination points
    """
    points: List[Point] = [
        Point(
            (
                random.randint(PADDING, WIDTH - PADDING),
                random.randint(PADDING, HEIGHT - PADDING)
            ),
            radius=5,
            color=(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
        )
        for _ in range(random.randint(5, 30))
    ]

    targets: List[Point] = [
        Point(
            (
                random.randint(PADDING, WIDTH - PADDING),
                random.randint(PADDING, HEIGHT - PADDING)
            ),
            radius=random.randint(3, 20),
            color=(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
        )
        for _ in range(random.randint(5, 30))
    ]

    return points, targets


# ---------------- ASSIGN TARGETS ----------------
def assign_targets(
    points: List[Point],
    targets: List[Point]
) -> Tuple[List[Point], List[Point], List[Point]]:
    """
    Assign targets to points.

    Handles mismatch:
    - If fewer points → duplicate
    - If more points → mark extras
    """
    extra_points: List[Point] = []

    if len(points) <= len(targets):
        # Duplicate points to match target count
        for _ in range(len(targets) - len(points)):
            new_point: Point = random.choice(points).copy()
            points.append(new_point)

        # One-to-one assignment
        for i in range(len(points)):
            points[i].setTarget(targets[i])

    else:
        # Assign targets cyclically
        for i in range(len(points)):
            points[i].setTarget(targets[i % len(targets)])

        # Mark extra points for removal
        extra_points = points[len(targets):]

    return points, targets, extra_points


# ---------------- MAIN ----------------
def main() -> None:
    """
    Main animation loop.

    Features:
    - Random point generation
    - Smooth transitions
    - Dynamic target reassignment
    - Continuous morphing
    """

    pygame.init()

    WIDTH: int = 1000
    HEIGHT: int = 800

    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Move Points")

    clock: pygame.time.Clock = pygame.time.Clock()

    # -------- INITIAL SETUP --------
    points, targets = generate_points(WIDTH, HEIGHT)
    points, targets, extra_points = assign_targets(points, targets)

    # # Add initial "explosion" effect
    # for point in points:
    #     point.setVelocity(
    #         random.uniform(-10, 10),
    #         random.uniform(-10, 10)
    #     )
    #     point.transition_timer = 15

    running: bool = True
    while running:

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # SPACE → regenerate system
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    points, targets = generate_points(WIDTH, HEIGHT)
                    points, targets, extra_points = assign_targets(points, targets)

        # ---------------- UPDATE ----------------
        for point in points:
            # # Delay steering for bounce effect
            # if point.transition_timer > 0:
            #     point.transition_timer -= 1
            # else:
            #     point.steer()

            point.steer()
            point.update()

        # Remove extra points only after reaching targets
        points = [
            p for p in points
            if not (p in extra_points and p.reached_target)
        ]

        # Optional: update targets (if animated)
        for target in targets:
            target.update()

        # -------- AUTO TRANSITION --------
        if len(points) > 0 and all(p.reached_target for p in points):
            # Generate new targets only
            _, targets = generate_points(WIDTH, HEIGHT)

            # # Apply random impulse (bounce effect)
            # for point in points:
            #     point.setVelocity(
            #         random.uniform(-10, 10),
            #         random.uniform(-10, 10)
            #     )
            #     point.transition_timer = 15

            # Reassign
            points, targets, extra_points = assign_targets(points, targets)

        # ---------------- DRAW ----------------
        screen.fill(BLACK)

        for target in targets:
            target.show(screen)

        for point in points:
            point.show(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()