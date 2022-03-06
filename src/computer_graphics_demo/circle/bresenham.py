"""
computer_graphics_demo.circle.bresenham
=======================================

Bresenham algorithm.
"""
import taichi as ti
from . import set8pixel


@ti.func
def circle(R: int, G: int, B: int, x0: int, y0: int, r: int):
    """circle.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param x0:
    :type x0: int
    :param y0:
    :type y0: int
    :param r:
    :type r: int
    """
    x, y = 0, r

    p = 3 - 2 * r
    while x <= y:
        if p < 0:
            p += 4 * x + 6
        else:
            y -= 1
            p += 4 * x - 4 * y + 10
        set8pixel(x0, y0, x, y, R, G, B)
        x += 1


@ti.kernel
def paint(R: int, G: int, B: int, x0: int, y0: int, r: int):
    """paint.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param x0:
    :type x0: int
    :param y0:
    :type y0: int
    :param r:
    :type r: int
    """
    circle(R, G, B, x0, y0, r)
