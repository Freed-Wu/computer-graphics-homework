"""
computer_graphics_demo.reality
==============================

Draw a scene by hidden surface removal, mirror reflection, texture, etc.
"""
import taichi as ti
import numpy as np
import math
import random
import itertools
from . import pixels

# 0: x0, 1: y0, 2: z0, 3: r, 4: type, 5: R, 6: G, 7: B
# type = 0: diffuse reflection
# type = 1: mirror reflection
# type = 2: refraction, 5: refreaction rate
spheres = ti.Vector.field(8, float)


def init():
    """init."""
    # earth
    spheres[0] = np.array([0.0, -1000.0, 0.0, 1000.0, 0.0, 0.5, 0.5, 0.5])
    # diffuse reflection example
    spheres[1] = np.array([-4.0, 1.0, 0.0, 1.0, 0.0, 0.4, 0.2, 0.1])
    # refraction example
    # you will see a reversal graph through a transparent ball
    # https://img-blog.csdn.net/20170114205419889?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvbGliaW5nX3plbmc=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center
    spheres[2] = np.array([4.0, 1.0, 0.0, 1.0, 2.0, 1.5, 0.0, 0.0])
    # mirror reflection example
    spheres[3] = np.array([0.0, 1.0, 0.0, 1.0, 1.0, 0.7, 0.6, 0.5])
    k, y, ran = 4, 0.5, range(-10, 10, 6)
    for x, z in itertools.product(ran, ran):
        refract_type = random.randint(0, 2)
        spheres[k] = np.array(
            [
                x,
                y,
                z,
                y,
                refract_type,
                random.random() if refract_type == 2 else random.random() + 1,
                random.random(),
                random.random(),
            ],
        )
        k += 1


nx = 1024
ny = 512
lookfrom = np.array([6.5, 1.5, 2.0])
lookat = np.array([0.0, 0.0, 0.0])
up = np.array([0.0, 1.0, 0.0])
view_dir = lookfrom - lookat
dist_to_focus = np.sqrt((view_dir * view_dir).sum())  # type: ignore


def normalize(n):
    """normalize.

    :param n:
    """
    return n / math.sqrt(np.dot(n, n))


# u, v, w is unit vector of relative coordinate
# u is horizontal
# v is vertical
w = normalize(view_dir)
u = normalize(np.cross(up, w))
v = np.cross(w, u)
# make sure the watching scope is suit
horizontal = u * 2 * dist_to_focus
vertical = v * 2 * ny / nx * dist_to_focus


@ti.func
def unit_vector(v):
    """unit_vector.

    :param v:
    """
    k = 1 / (ti.sqrt(v.dot(v)))
    return k * v


@ti.func
def reflect(v, n):
    """reflect.

    https://en.wikipedia.org/wiki/Specular_reflection

    :param v:
    :param n:
    """
    return v - 2 * v.dot(n) * n


@ti.func
def refract(v, n, ni_over_nt):
    """refract.

    https://en.wikipedia.org/wiki/Snell%27s_law

    :param v:
    :param n:
    :param ni_over_nt:
    """
    dt = v.dot(n)
    discriminant = 1.0 - ni_over_nt * ni_over_nt * (1.0 - dt * dt)
    succ = False
    refracted = ti.Vector([0.0, 0.0, 0.0])
    if discriminant > 0:
        refracted = ni_over_nt * (v - n * dt) - n * ti.sqrt(discriminant)
        succ = True
    return succ, refracted


@ti.func
def schlick(cosine, ni_over_nt):
    """schlick.

    https://en.wikipedia.org/wiki/Schlick%27s_approximation

    :param cosine:
    :param ref_idx:
    """
    # cosine must > 0, or result will > 1
    # however, result is reflection coefficient
    # i.e., ratio of the amplitude of the reflected wave to the incident wave
    # must < 1
    # wikipedia is not fully correct.
    cosine = ti.abs(cosine)
    r0 = ((1 - ni_over_nt) / (1 + ni_over_nt)) ** 2
    return r0 + (1 - r0) * ti.pow((1 - cosine), 5)


@ti.func
def random_in_unit_sphere():
    """random_in_unit_sphere.

    http://www.pbr-book.org/3ed-2018/Monte_Carlo_Integration/2D_Sampling_with_Multidimensional_Transformations.html
    """
    eta1, eta2 = ti.random(), ti.random()
    coeff = 2 * ti.sqrt(eta1 * (1 - eta1))
    eta2m2pi = eta2 * math.pi * 2
    return ti.Vector(
        [ti.cos(eta2m2pi) * coeff, ti.sin(eta2m2pi) * coeff, 1 - 2 * eta1]
    )


@ti.func
def hit_sphere(center, radius, rayo, rayd, mint, maxt):
    """hit_sphere.

    :param center:
    :param radius:
    :param rayo:
    :param rayd:
    :param mint:
    :param maxt:
    """
    rst = False
    t = 0.0
    oc = rayo - center
    a = rayd.dot(rayd)
    b = 2.0 * oc.dot(rayd)
    c = oc.dot(oc) - radius * radius
    disc = b * b - 4.0 * a * c
    if disc >= 0:
        sq = ti.sqrt(disc)
        t = (-b - sq) / (2.0 * a)
        if t > mint and t < maxt:
            rst = True
        else:
            t = (-b + sq) / (2.0 * a)
            if t > mint and t < maxt:
                rst = True

    return rst, t, rayo + t * rayd


@ti.func
def hit_spheres(rayo, rayd, mint, maxt):
    """hit_spheres.

    :param rayo:
    :param rayd:
    :param mint:
    :param maxt:
    """
    rst = False
    rt = 1e10
    hit_point = ti.Vector([0.0, 0.0, 0.0])
    normal = ti.Vector([0.0, 0.0, 0.0])
    index = -1
    for i in ti.static(range(20)):
        sc = ti.Vector([spheres[i][0], spheres[i][1], spheres[i][2]])
        r = spheres[i][3]
        hit, t, hitp = hit_sphere(sc, r, rayo, rayd, mint, maxt)
        if hit and t < rt:
            rst = True
            rt = t
            normal = unit_vector(hitp - sc)
            hit_point = hitp
            index = i
    return rst, hit_point, normal, index


@ti.func
def color(start, dir):
    """color.

    :param start:
    :param dir:
    """
    rst = ti.Vector([1.0, 1.0, 1.0])
    count = 0
    while count < 10:
        hit, hit_point, n, index = hit_spheres(start, dir, 0.001, 1e10)
        if hit:
            # hit_point is next start point of ray
            start = hit_point
            if spheres[index][4] <= 1.0:
                albedo = ti.Vector(
                    [spheres[index][5], spheres[index][6], spheres[index][7]]
                )
                rst = rst * albedo
                if spheres[index][4] == 0.0:
                    dir = unit_vector(n + random_in_unit_sphere())
                elif spheres[index][4] == 1.0:
                    dir = reflect(dir, n)
            else:
                cosine = dir.dot(n)
                # ray comes from outer to inner
                # outward_n in the semi-space where incident vector exists
                outward_n = n
                ni_over_nt = 1.0 / spheres[index][5]
                # ray comes from inner to outer
                if cosine > 0:
                    outward_n = -n
                    ni_over_nt = spheres[index][5]
                succ, refracted = refract(dir, outward_n, ni_over_nt)
                if succ:
                    reflect_prob = schlick(cosine, ni_over_nt)
                    # reflect_prob is < 10%, so refraction is major
                    # reflection only make the ray dim
                    if ti.random() < reflect_prob:
                        dir = reflect(dir, n)
                    else:
                        dir = refracted
                # full reflect
                else:
                    dir = reflect(dir, n)
            count += 1
        else:
            t = 0.5 * (dir[1] + 1.0)
            skycolor = (1.0 - t) * ti.Vector([1.0, 1.0, 1.0]) + t * ti.Vector(
                [0.5, 0.7, 1.0]
            )
            rst = rst * skycolor
            break
    return rst


@ti.kernel
def paint(R: int, G: int, B: int, sample_number: int, r_aperture: float):
    """paint.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param sample_number:
    :type sample_number: int
    :param r_aperture:
    :type r_aperture: float
    """
    for i, j in pixels:
        col = ti.Vector([0.0, 0.0, 0.0])
        for _ in range(sample_number):
            # change vector of uOv plane to Oxyz
            uu = float(i) / float(nx)
            vv = float(j) / float(ny)
            uv = ti.Vector([uu, vv])
            # use a random offset to reduce sawtooth
            # use another random distribution is possible
            # e.g., vector norm is ti.random()
            # and theta is ti.random() * 2 * math.pi
            offset = r_aperture * ti.Vector([ti.random(), ti.random()]).dot(uv)
            direction = (
                uu * ti.Vector(horizontal)
                + vv * ti.Vector(vertical)
                - ti.Vector(horizontal + vertical) / 2
                - ti.Vector(lookfrom)
                - offset
            )
            col += color(ti.Vector(lookfrom) + offset, unit_vector(direction))
        pixels[i, j] = col / sample_number
