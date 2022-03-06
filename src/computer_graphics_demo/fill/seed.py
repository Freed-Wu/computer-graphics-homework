"""
computer_graphics_demo.fill.seed
================================

Seed point algorithm.
"""
from ..line import polygon
from ..line.bresenham import line
from .. import pixels, setpixel


def paint(R: int, G: int, B: int, x_seed: int, y_seed: int, *argv: int):
    """paint.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param x_seed:
    :type x_seed: int
    :param y_seed:
    :type y_seed: int
    :param argv:
    :type argv: int
    """
    if len(argv) % 2:
        exit(f"point number must be even, now is {len(argv)}")
    elif len(argv) < 6:
        exit(f"point number must be greater than 3, now is {len(argv)}")
    polygon(R, G, B, *argv, isclose=True, line=line)

    stack = [(x_seed, y_seed)]
    while len(stack):
        x, y = stack[0]
        setpixel(x, y, R, G, B)
        stack.remove((x, y))
        for i, j in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            x2, y2 = x + i, y + j
            # pixels[x2, y2] have already been colorified
            if (
                pixels[x2, y2][0]
                or pixels[x2, y2][1]
                or pixels[x2, y2][2]
                or set(stack) | {(x2, y2)} == set(stack)
            ):
                continue
            stack += [(x2, y2)]
