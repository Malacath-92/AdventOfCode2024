import math
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(lhs, rhs):
        return Vector(lhs.x + rhs.x, lhs.y + rhs.y)

    def __sub__(lhs, rhs):
        return Vector(lhs.x - rhs.x, lhs.y - rhs.y)

    def __mul__(lhs, rhs: int):
        return Vector(lhs.x * rhs, lhs.y * rhs)

    def __truediv__(lhs, rhs: int):
        return Vector(lhs.x / rhs, lhs.y / rhs)

    def __str__(self):
        return f"{self.x},{self.y}"

    def __repl__(self):
        return f"Vector({self.x=},{self.y=})"

    def len(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
