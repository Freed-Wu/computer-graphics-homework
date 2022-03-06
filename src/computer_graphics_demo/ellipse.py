"""
computer_graphics_demo.ellipse
==============================

Draw a ellipse.
"""
import taichi as ti
from .circle import set4pixel


@ti.func
def ellipse(R: int, G: int, B: int, x0: int, y0: int, a0: int, b0: int):
    """ellipse.

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
    :param a:
    :type a: int
    :param b:
    :type b: int
    """
    a, b = ti.min(a0, b0), ti.max(a0, b0)
    x, y, p = 0, b, b ** 2 - b * a ** 2 - a ** 2 / 4

    while x * b ** 2 <= y * a ** 2:
        if p < 0:
            p += 2 * x * b ** 2 + 3 * b ** 2
        else:
            p += 2 * x ** b * 2 - 2 * y * a ** 2 + 3 * b ** 2 + 2 * a ** 2
            y -= 1
        if a == a0:
            set4pixel(x0, y0, x, y, R, G, B)
        else:
            set4pixel(x0, y0, y, x, R, G, B)
        x += 1
    q = (b * (x + 1 / 2)) ** 2 + (a * (y - 1)) ** 2 - (a * b) ** 2
    while y >= 0:
        if q < 0:
            q += 3 * a ** 2 + 2 * b ** 2 + 2 * x * b ** 2 - 2 * y * a ** 2
            x += 1
        else:
            q += 3 * a ** 2 - 2 * y * a ** 2
        if a == a0:
            set4pixel(x0, y0, x, y, R, G, B)
        else:
            set4pixel(x0, y0, y, x, R, G, B)
        y -= 1


@ti.kernel
def paint(R: int, G: int, B: int, x0: int, y0: int, a: int, b: int):
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
    :param a:
    :type a: int
    :param b:
    :type b: int
    """
    ellipse(R, G, B, x0, y0, a, b)
