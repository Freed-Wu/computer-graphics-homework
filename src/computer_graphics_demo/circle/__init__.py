"""
computer_graphics_demo.circle
=============================

Draw a circle.
"""
from .. import setpixel


def set4pixel(x0, y0, x, y, R, G, B):
    """set4pixel.

    :param x0:
    :param y0:
    :param x:
    :param y:
    :param R:
    :param G:
    :param B:
    """
    setpixel(x0 + x, y0 + y, R, G, B)
    setpixel(x0 - x, y0 + y, R, G, B)
    setpixel(x0 + x, y0 - y, R, G, B)
    setpixel(x0 - x, y0 - y, R, G, B)


def set8pixel(x0, y0, x, y, R, G, B):
    """set8pixel.

    :param x0:
    :param y0:
    :param x:
    :param y:
    :param R:
    :param G:
    :param B:
    """
    set4pixel(x0, y0, x, y, R, G, B)
    set4pixel(x0, y0, y, x, R, G, B)
