"""
computer_graphics_demo.mandelbrot
=================================

Draw a Mandelbrot set
"""
import taichi as ti
from . import pixels, setpixel

n = 512


@ti.func
def complex_sqr(z) -> ti.Vector:
    """complex_sqr.

    :param z:
    """
    return ti.Vector([z[0] ** 2 - z[1] ** 2, z[1] * z[0] * 2])


@ti.kernel
def paint(R: int, G: int, B: int, scale: float, iteration_max: int):
    """paint.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param scale:
    :type scale: float
    :param iteration_max:
    :type iteration_max: int
    """
    for i, j in pixels:
        c = ti.Vector([i / n - 1, j / n - 0.5]) * scale
        iterations = 0
        z = ti.Vector([0.0, 0.0])
        while z.norm() < 20 and iterations <= iteration_max:
            z = complex_sqr(z) + c
            iterations += 1
        if iterations > iteration_max:
            setpixel(i, j, R, G, B)
