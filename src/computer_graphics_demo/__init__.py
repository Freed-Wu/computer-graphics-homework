"""
computer_graphics_demo
======================

Common functions.
"""
import logging
from typing import Final

import taichi as ti

logger = logging.getLogger(__name__)

try:
    from get_version import get_version, NoVersionFound

    try:
        __version__ = get_version(__file__)
    except NoVersionFound:
        __version__ = "0.0.0"
except ImportError:
    logger.warning("Please install get_version!")
    __version__ = "0.0.0"

_binname: Final = "cgdemo"
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
