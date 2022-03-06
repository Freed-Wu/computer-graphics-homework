"""
computer_graphics_demo.bezier
=============================

Draw a Bezier curve.
"""
import taichi as ti
from .line import polygon
from .line.bresenham import line


def basis(i: int, degree: int, u: float) -> float:
    """basis.

    :param i:
    :type i: int
    :param degree:
    :type degree: int
    :param u:
    :type u: float
    :rtype: float
    """
    if i > degree:
        return 0
    elif i == 0:
        return (1 - u) ** degree
    elif i == 1:
        return degree * u * (1 - u) ** (degree - 1)
    return basis(degree - 1, i, u) * (1 - u) + basis(degree - 1, i - 1, u) * u


def paint(R: int, G: int, B: int, sample_number: int, *argv: int) -> None:
    """paint.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param sample_number:
    :type sample_number: int
    :param argv:
    :type argv: int
    :rtype: None
    """
    xs = argv[::2]
    ys = argv[1::2]
    if len(argv) % 2:
        exit(f"point number must be even, now is {len(argv)}")
    argv2 = []
    for u in range(0, sample_number):
        x, y = 0, 0
        for i in range(len(xs)):
            x += xs[i] * basis(i, len(xs) - 1, u / sample_number)
            y += ys[i] * basis(i, len(xs) - 1, u / sample_number)
        argv2 += [ti.floor(x), ti.floor(y)]
    polygon(R, G, B, *argv2, line=line)
