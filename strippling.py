import cv2
import numpy as np
import os
import json
import hashlib

# -------- SETTINGS --------
IMAGE_PATH = "images/baby.jpg"
NUM_POINTS = 6000
ITERATIONS = 25

WINDOW_HEIGHT = 800
PADDING = 20

def generate_stippling_points(
    image_path: str,
    num_points: int = 3000,
    iterations: int = 25,
    output_height: int = 500
):
    # -------- LOAD IMAGE --------
    img = cv2.imread(image_path)

    h0, w0 = img.shape[:2]
    scale = output_height / h0
    new_w = int(w0 * scale)
    new_h = output_height

    img = cv2.resize(img, (new_w, new_h))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)

    h, w = gray.shape

    # -------- DENSITY --------
    density = 1 - (gray / 255.0)

    flat_density = density.flatten()
    flat_density /= flat_density.sum()

    # -------- INITIAL POINTS --------
    points = np.column_stack((
        np.random.randint(0, w, num_points),
        np.random.randint(0, h, num_points)
    )).astype(float)

    # -------- SAMPLING FUNCTION --------
    def weighted_sample():
        indices = np.random.choice(len(flat_density), size=num_points * 5, p=flat_density)
        ys, xs = np.unravel_index(indices, (h, w))
        return list(zip(xs, ys))

    # -------- RELAXATION --------
    for _ in range(iterations):
        clusters = [[] for _ in range(num_points)]
        samples = weighted_sample()

        for sx, sy in samples:
            dists = np.sum((points - [sx, sy])**2, axis=1)
            idx = np.argmin(dists)
            clusters[idx].append([sx, sy])

        for i, cluster in enumerate(clusters):
            if len(cluster) > 0:
                cluster = np.array(cluster)
                points[i] = cluster.mean(axis=0)

    # -------- GENERATE OUTPUT DATA --------
    result = []

    for x, y in points:
        x_i, y_i = int(x), int(y)

        # safety clamp
        x_i = max(0, min(w-1, x_i))
        y_i = max(0, min(h-1, y_i))

        brightness = gray[y_i, x_i]

        # better radius scaling
        radius = int(((255 - brightness) / 40))

        # Get color from original image (BGR → RGB)
        b, g, r = img[y_i, x_i]
        color = [int(r), int(g), int(b)]

        if radius > 0:
            result.append((x_i, y_i, radius, color))

    return result, (w, h)


def get_stippling_points(
    image_path: str,
    num_points: int = 3000,
    iterations: int = 25,
    output_height: int = 500
):
    # -------- CREATE FOLDER --------
    os.makedirs("stipplings", exist_ok=True)

    # -------- CREATE UNIQUE KEY --------
    key_string = f"{image_path}_{num_points}_{iterations}_{output_height}"
    key_hash = hashlib.md5(key_string.encode()).hexdigest()

    file_path = os.path.join("stipplings", f"{key_hash}.json")

    # -------- LOAD IF EXISTS --------
    if os.path.exists(file_path):
        print("Loading cached stippling...")
        with open(file_path, "r") as f:
            data = json.load(f)
            return data  # list of [x, y, r]

    # -------- GENERATE --------
    print("Generating stippling...")
    points = generate_stippling_points(
        image_path,
        num_points,
        iterations,
        output_height
    )

    # -------- SAVE --------
    # convert tuples → lists (json doesn't support tuples)
    serializable = [list(p) for p in points]

    with open(file_path, "w") as f:
        json.dump(serializable, f)

    return serializable

if __name__ == "__main__":    
    import pygame
    
    pygame.init()

    points , (w,h) = get_stippling_points(IMAGE_PATH)

    screen = pygame.display.set_mode((w,h))
    pygame.display.set_caption("voronoi stippling")

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        screen.fill((255, 255, 255))

         # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for x,y,r in points:
            pygame.draw.circle(screen, (0,0,0), (x,y), r)

        pygame.display.flip()

    pygame.quit()