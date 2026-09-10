from __future__ import annotations

from Vector import Vector
from typing import Tuple, Optional
import pygame

# ---------------- CONSTANTS ----------------
WHITE: Tuple[int, int, int] = (255, 255, 255)


def map_value(
    value: float,
    in_min: float,
    in_max: float,
    out_min: float,
    out_max: float
) -> float:
    """
    Linearly maps a value from one range to another with clamping.

    Example:
        map_value(5, 0, 10, 0, 100) -> 50
    """
    if in_max == in_min:
        return out_min

    # Normalize value to 0–1
    t: float = (value - in_min) / (in_max - in_min)

    # Clamp between 0 and 1
    t = max(0.0, min(1.0, t))

    # Scale to output range
    return out_min + t * (out_max - out_min)


class Point:
    """
    Represents a moving particle that:
    - Moves using steering behavior
    - Transitions toward a target point
    - Interpolates radius and color based on distance
    """

    def __init__(
        self,
        pos: Tuple[float, float],
        target: Optional[Point] = None,
        radius: int = 5,
        color: Tuple[int, int, int] = WHITE,
    ) -> None:
        # ---------------- PHYSICS ----------------
        self.pos: Vector = Vector(*pos)     # current position
        self.vel: Vector = Vector()         # velocity
        self.acc: Vector = Vector()         # acceleration

        # ---------------- TARGET ----------------
        self.target: Optional[Point] = target

        # Distance to target (used for interpolation scaling)
        self.target_dist: float = 1.0
        if self.target:
            self.target_dist = self.pos.distance_to(self.target.pos)

        # ---------------- SIZE ----------------
        self.base_radius: int = radius      # original size
        self.curr_radius: float = radius    # animated size

        # ---------------- COLOR ----------------
        self.color: Tuple[int, int, int] = color        # base color
        self.curr_color: Tuple[int, int, int] = color   # animated color

        # ---------------- MOTION LIMITS ----------------
        self.maxspeed: float = 10.0
        self.maxacc: float = 5.0

        # ---------------- STATE ----------------
        self.reached_target: bool = False
        self.transition_timer: int = 0  # delay steering for bounce effect

    # ---------------- SETTERS ----------------
    def setVelocity(self, x: float, y: float) -> None:
        """Set velocity vector directly."""
        self.vel = Vector(x, y)

    def setAcceleration(self, x: float, y: float) -> None:
        """Set acceleration vector directly."""
        self.acc = Vector(x, y)

    def setTarget(self, target: Point) -> None:
        """
        Assign a new target for the point and reset transition state.
        """
        self.target = target
        if target:
            self.target_dist = self.pos.distance_to(target.pos)
            self.reached_target = False

    def setPos(self, x: float, y: float) -> None:
        """Set position directly."""
        self.pos = Vector(x, y)

    def getPos(self) -> Tuple[float, float]:
        """Return current position as tuple."""
        return (self.pos.x, self.pos.y)

    # ---------------- UTILITY ----------------
    def copy(self) -> Point:
        """
        Create a shallow copy of the point (used for duplicating particles).
        """
        new_point = Point(
            self.getPos(),
            self.target,
            self.base_radius,
            self.color,
        )
        if self.target:
            new_point.target_dist = new_point.pos.distance_to(self.target.pos)
        return new_point

    # ---------------- RENDER ----------------
    def show(self, screen: pygame.Surface) -> None:
        """Draw the point on the screen."""
        pygame.draw.circle(
            screen,
            self.curr_color,
            self.pos.to_tuple(),
            int(self.curr_radius),
        )

    # ---------------- UPDATE ----------------
    def update(self) -> None:
        """
        Update physics, size interpolation, and color interpolation.
        """
        # -------- PHYSICS --------
        self.vel += self.acc

        # Limit velocity
        if self.vel.magnitude() > self.maxspeed:
            self.vel = self.vel.set_magnitude(self.maxspeed)

        self.pos += self.vel
        self.acc = Vector(0, 0)

        # No target → no interpolation
        if not self.target:
            return

        # -------- DISTANCE --------
        dist: float = self.pos.distance_to(self.target.pos)

        # -------- SIZE INTERPOLATION --------
        self.curr_radius = map_value(
            dist,
            0,
            self.target_dist,
            self.target.curr_radius,
            self.base_radius,
        )

        # -------- COLOR INTERPOLATION --------
        rt, gt, bt = self.target.color   # target color
        r, g, b = self.color            # original color

        newr: int = int(map_value(dist, 0, self.target_dist, rt, r))
        newg: int = int(map_value(dist, 0, self.target_dist, gt, g))
        newb: int = int(map_value(dist, 0, self.target_dist, bt, b))

        self.curr_color = (newr, newg, newb)

        # -------- SNAP TO TARGET --------
        if dist < 3 and not self.reached_target:
            self.reached_target = True

            # Snap position
            self.setPos(*self.target.pos.to_tuple())

            # Match final size & color
            self.curr_radius = self.target.base_radius
            self.color = self.target.color
            self.curr_color = self.color

    # ---------------- STEERING ----------------
    def steer(self) -> None:
        """
        Apply steering force toward the target.
        Includes:
        - Smooth arrival
        """
        if not self.target:
            return

        desired_vel: Vector = self.target.pos - self.pos
        dist: float = desired_vel.magnitude()

        if dist == 0:
            return

        # -------- ARRIVAL BEHAVIOR --------
        if dist < 300:
            t: float = dist / 300
            desired_vel = desired_vel.set_magnitude(t * self.maxspeed)
        else:
            desired_vel = desired_vel.set_magnitude(self.maxspeed)

        # Apply steering force
        self.acc += desired_vel - self.vel

        # Limit acceleration
        if self.acc.magnitude() > self.maxacc:
            self.acc = self.acc.set_magnitude(self.maxacc)