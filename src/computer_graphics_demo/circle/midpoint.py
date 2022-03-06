"""
computer_graphics_demo.circle.midpoint
======================================

Midpoint algorithm.
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

    p = 5 / 4 - r
    while x <= y:
        if p < 0:
            p += 2 * x + 3
        else:
            p += 2 * x - 2 * y + 5
            y -= 1
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
