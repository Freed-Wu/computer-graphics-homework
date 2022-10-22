# noqa: D400 D205
"""
computer_graphics_demo
======================

Common functions.
"""
import taichi as ti
from typing import Final

try:
    from get_version import get_version, NoVersionFound

    try:
        __version__ = get_version(__file__)
    except NoVersionFound:
        __version__ = "0.0.0"
except ImportError:
    __version__ = "0.0.0"

_binname: Final = "cgdemo"
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
