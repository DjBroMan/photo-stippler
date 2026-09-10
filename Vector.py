from __future__ import annotations

import math
from typing import Tuple


class Vector:
    """
    2D Vector class supporting basic vector math,
    used for physics and particle systems.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x: float = float(x)
        self.y: float = float(y)

    # -------------------------
    # String Representation
    # -------------------------
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    # -------------------------
    # Basic Operations
    # -------------------------
    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector:
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vector:
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Vector:
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector(self.x / scalar, self.y / scalar)

    # -------------------------
    # In-place Operations
    # -------------------------
    def __iadd__(self, other: Vector) -> Vector:
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other: Vector) -> Vector:
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, scalar: float) -> Vector:
        self.x *= scalar
        self.y *= scalar
        return self

    def __itruediv__(self, scalar: float) -> Vector:
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        self.x /= scalar
        self.y /= scalar
        return self

    # -------------------------
    # Magnitude & Normalization
    # -------------------------
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self) -> Vector:
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0)
        return self / mag

    def set_magnitude(self, scalar: float) -> Vector:
        """
        Returns a new vector with same direction but given magnitude.
        """
        return self.normalize() * scalar

    # -------------------------
    # Dot Product
    # -------------------------
    def dot(self, other: Vector) -> float:
        return self.x * other.x + self.y * other.y

    # -------------------------
    # Distance
    # -------------------------
    def distance_to(self, other: Vector) -> float:
        return (self - other).magnitude()

    # -------------------------
    # Angle
    # -------------------------
    def angle(self) -> float:
        return math.atan2(self.y, self.x)

    def angle_between(self, other: Vector) -> float:
        mag1 = self.magnitude()
        mag2 = other.magnitude()

        if mag1 == 0 or mag2 == 0:
            return 0.0

        dot = self.dot(other)
        cos_theta = max(-1.0, min(1.0, dot / (mag1 * mag2)))  # clamp
        return math.acos(cos_theta)

    # -------------------------
    # Utility
    # -------------------------
    def copy(self) -> Vector:
        return Vector(self.x, self.y)

    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)