"""
computer_graphics_demo.line.midpoint
====================================

Midpoint algorithm.
"""
import taichi as ti
from .. import setpixel
from . import polygon


@ti.pyfunc
def line(R: int, G: int, B: int, x1: int, y1: int, x2: int, y2: int):
    """line.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param x1:
    :type x1: int
    :param y1:
    :type y1: int
    :param x2:
    :type x2: int
    :param y2:
    :type y2: int
    """
    m = 100
    if x2 != x1:
        m = (y2 - y1) / (x2 - x1)

    u1, u2, v1, v2 = x1, x2, y1, y2
    if ti.abs(m) > 1:
        u1, u2, v1, v2 = y1, y2, x1, x2
    if u1 > u2:
        u1, u2, v1, v2 = u2, u1, v2, v1
    a, b = ti.abs(v2 - v1), u1 - u2
    p = a + 0.5 * b
    u, v = u1, v1
    while u < u2:
        if p < 0:
            p += a
        else:
            p += a + b
            if m > 0:
                v += 1
            else:
                v -= 1
        if ti.abs(m) <= 1:
            setpixel(u, v, R, G, B)
        else:
            setpixel(v, u, R, G, B)
        u += 1


def paint(R: int, G: int, B: int, *argv: int) -> None:
    """paint.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param argv:
    :type argv: int
    :rtype: None
    """
    polygon(R, G, B, *argv, line=line)
