import os
import pygame
import random
from typing import List, Tuple
from Point import Point
from strippling import get_stippling_points

# ---------------- SETTINGS ----------------
WIDTH: int = 1000
HEIGHT: int = 800

BG: Tuple[int, int, int] = (0, 0, 0)
POINT_COLOR: Tuple[int, int, int] = (0, 150, 255)

IMAGE_FOLDER: str = "images"

# ---------------- LOAD IMAGE PATHS ----------------
image_paths: List[str] = [
    os.path.join(IMAGE_FOLDER, f)
    for f in os.listdir(IMAGE_FOLDER)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

image_paths.sort()
assert len(image_paths) > 0, "No images found in images/ folder"


# ---------------- LOAD STIPPLING ----------------
def load_stippling(image_path: str) -> List[Point]:
    """
    Loads stippling data for an image and converts it into Point objects.
    Also scales and centers the points to fit the Pygame window.
    """
    points_data, (w, h) = get_stippling_points(image_path)

    # -------- SCALE TO FIT SCREEN --------
    scale: float = min(
        (WIDTH - 100) / w,
        (HEIGHT - 100) / h
    )

    offset_x: float = (WIDTH - w * scale) // 2
    offset_y: float = (HEIGHT - h * scale) // 2

    targets: List[Point] = []

    for x, y, r, color in points_data:
        # Scale + center position
        tx: float = x * scale + offset_x
        ty: float = y * scale + offset_y

        # Scale radius (ensure minimum size)
        tr: int = max(1, int(r * scale))

        # Create target point with color
        targets.append(
            Point(
                (tx, ty),
                radius=tr,
                color=tuple(color)  # convert JSON list → tuple
            )
        )

    return targets


# ---------------- ASSIGN TARGETS ----------------
def assign_targets(
    points: List[Point],
    targets: List[Point]
) -> Tuple[List[Point], List[Point]]:
    """
    Assigns each point a target.
    
    Handles mismatch in counts:
    - If fewer points → duplicate points
    - If more points → mark extras for removal
    """
    extra_points: List[Point] = []

    if len(points) <= len(targets):
        # Duplicate points if needed
        for _ in range(len(targets) - len(points)):
            new_point: Point = random.choice(points).copy()
            points.append(new_point)

        # Assign one-to-one targets
        for i in range(len(points)):
            points[i].setTarget(targets[i])

    else:
        # Assign targets cyclically
        for i in range(len(points)):
            points[i].setTarget(targets[i % len(targets)])

        # Mark extra points for later deletion
        extra_points = points[len(targets):]

    return points, extra_points


# ---------------- MAIN ----------------
def main() -> None:
    """
    Main application loop.
    
    Handles:
    - Image transitions
    - Particle updates
    - Rendering
    """
    pygame.init()

    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stippling Morph")

    clock: pygame.time.Clock = pygame.time.Clock()

    current_index: int = 0

    # -------- INITIAL LOAD --------
    targets: List[Point] = load_stippling(image_paths[current_index])

    # Create initial random particles
    points: List[Point] = [
        Point(
            (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
            radius=3,
            color= (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        )
        for _ in range(len(targets))
    ]

    # Assign initial targets
    points, extra_points = assign_targets(points, targets)

    # Add initial "explosion" effect
    for point in points:
        point.setVelocity(
            random.uniform(-10, 10),
            random.uniform(-10, 10)
        )
        point.transition_timer = 15

    transitioning: bool = True  # prevents spam switching

    running: bool = True
    while running:

        # ---------------- EVENTS ----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # SPACE → switch image (only when stable)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not transitioning:

                    # Apply random impulse (bounce effect)
                    for point in points:
                        point.setVelocity(
                            random.uniform(-10, 10),
                            random.uniform(-10, 10)
                        )
                        point.transition_timer = 15

                    # Move to next image
                    current_index = (current_index + 1) % len(image_paths)

                    targets = load_stippling(image_paths[current_index])
                    points, extra_points = assign_targets(points, targets)

                    transitioning = True  # lock input

        # ---------------- UPDATE ----------------
        for p in points:
            # Delay steering for bounce effect
            if p.transition_timer > 0:
                p.transition_timer -= 1
            else:
                p.steer()

            p.update()

        # Remove extra points after reaching target
        points = [
            p for p in points
            if not (p in extra_points and p.reached_target)
        ]

        # Check if transition is complete
        if len(points) > 0 and all(p.reached_target for p in points):
            transitioning = False

        # ---------------- DRAW ----------------
        screen.fill(BG)

        for p in points:
            p.show(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()