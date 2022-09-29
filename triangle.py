from dataclasses import dataclass
from time import perf_counter
import tkinter as tk
from math import sqrt, log2
from typing import List, Tuple
from secrets import token_hex

@dataclass(frozen=True, slots=True)
class Triangle:
    A: complex
    B: complex
    C: complex

    @property
    def dots(self) -> Tuple[complex, complex, complex]:
        return tuple(self.__getattribute__(atr) for atr in self.__dataclass_fields__)


def count_triangle(a: int, offset: complex = 0) -> Triangle:
    A = offset
    B = a + offset
    C = complex(a//2, round(sqrt(3*a**2/4))) + offset
    return Triangle(A, B, C)


def triangle_recursion(a: int, depth: int, offset: complex = 0) -> List[Triangle]:
    if depth == 0:
        return [count_triangle(a, offset), ]
    else:
        triangles = list()
        for point in count_triangle(a//2, offset).dots:
            triangles.extend(triangle_recursion(a//2, depth-1, offset=point))
        return triangles


def random_color() -> str:
    return '#'+token_hex(3)


def draw_triangle(triangle: Triangle, canvas: tk.Canvas, height: int) -> None:
    dots = [(p.real, height-p.imag) for p in triangle.dots]
    canvas.create_polygon(dots, fill=random_color())


def main():
    width = height = 1000
    pixels_per_triangle = 5

    root = tk.Tk()
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()

    offset = 1+50j
    length = min(width, height)
    depth = int(log2(length//pixels_per_triangle))
    for t in triangle_recursion(length, depth, offset):
        draw_triangle(t, canvas, height)

    root.mainloop()


if __name__ == "__main__":
    main()
