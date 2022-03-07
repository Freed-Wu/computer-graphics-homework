"""
computer_graphics_demo
======================

Common functions.
"""
import taichi as ti
from typing import Final

VERSION: Final = "0.0.2"
pixels = ti.Vector.field(3, float)


def init() -> None:
    """init.

    :rtype: None
    """
    pass


@ti.pyfunc
def setpixel(x: int, y: int, R: int, G: int, B: int):
    """setpixel.

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
