"""
computer_graphics_demo
======================

Common functions.
"""

import taichi as ti
import logging

logger = logging.getLogger(__name__)

pixels = ti.Vector.field(3, float)


def init():
    """Init."""
    pass


@ti.pyfunc
def setpixel(x: int, y: int, R: int, G: int, B: int):
    """Set Pixel.

    :param x:
    :type x: int
    :param y:
    :type y: int
    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    """
    pixels[x, y] = ti.Vector([R, G, B])
