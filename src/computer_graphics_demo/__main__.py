#! /usr/bin/env python3
# Docstring {{{ #
"""Computer graphics algorithms demonstration.

usage: cgdemo [-hVdns] [ [-v] | [-q|-qq] ] [-x <height>] [-y <width>] [-o <out>]
    [-c <color>] [-a <args>] [-t <time>] <command>

options:
    -h, --help              Show this screen.
    -V, --version           Show version.
    -d, --debug             Debug this program.
    -n, --dry-run           Don't show any canvas.
    -s, --second            Use second algorithm. See section algorithm.
    -v, --verbose           Output verbosity. (e.g., default arguments)
    -q, --quiet             Redirect stdout to null. Again for stderr.
    -x, --height <height>   Height of canvas. [default: 512]
    -y, --width <width>     Width of canvas. [default: 1024]
    -o, --output <out>      Save output to a file. See section output.
    -c, --color <color>     Color of graph. [default: 255,0,0]
    -a, --args <args>       Arguments. See section argument.
    -t, --timeout <time>    Auto exit. [default: 30]

commands:
    line                    Draw a line.
    circle                  Draw a circle.
    ellipse                 Draw a ellipse.
    fill                    Fill a region.
    bezier                  Draw a Bezier curve.
    b                       Draw a B-spline.
    koch                    Draw a Koch curve.
    mandelbrot              Draw a Mandelbrot set.
    julia                   Draw a Julia set.
    fern                    Draw a fern.
    reality                 Draw a scene by hidden surface removal, mirror
                            reflection, texture, etc.

output: (%d is format string)
    *%d*.png
    *%d*.jpg
    *%d*.bmp
    */video.mp4
    */video.gif

algorithm:
                default                     second
    line        midpoint                    bresenham
    circle      midpoint                    bresenham
    ellipse     midpoint
    fill        scan                        seed
    bezier      Bezier
    b           De_Boor
    koch        Lindenmayer_system
    mandelbrot  f(z)=z*z+c
    julia       f(z)=z*z+c
    fern        iterated_fuction_system
    reality     ray_tracing

argument:
    line        x1,y1,x2,y2,...
    circle      x0,y0,r
    ellipse     x0,y0,a,b
    fill (scan) x1,y1,x2,y2,x3,y3,...
    fill (seed) x_seed,y_seed,x1,y1,x2,y2,x3,y3,...
    bezier      sample_number,x1,y1,...
    b           degree,x1,y1,...
    koch        scale,iteration_max,x0,y0
    mandelbrot  scale,iteration_max
    julia       scale,iteration_max
    fern        scale,iteration_max,x0,y0
    reality     sample_number,r_aperture
"""
# }}} Docs #
from typing import Optional, Dict, Union
from pprint import pformat
import logging
from docopt import docopt
from . import VERSION

Arg = Optional[Union[bool, int, str]]
logger = logging.getLogger(__name__)


def main(doc: str = __doc__):  # type: ignore
    """Run main function."""
    try:
        args: Dict[str, Arg] = docopt(doc, version=VERSION)
    except Exception:
        args = {}
    if args.get("--debug"):
        try:
            from rich.logging import RichHandler

            logging.basicConfig(
                level="DEBUG",
                format="%(message)s",
                handlers=[RichHandler(rich_tracebacks=True, markup=True)],
            )
        except ImportError:
            logging.basicConfig(level="DEBUG")
    logger.debug(pformat(args))
    # Parse {{{ #
    import os
    import taichi as ti

    if args["--quiet"]:
        import sys

        sys.stdout = open(os.devnull, "w")
        if args["--quiet"] > 1:  # type: ignore
            sys.stderr = sys.stdout

    R, G, B = list(map(int, args["--color"].split(",")))  # type: ignore
    if args["--args"]:
        argv = list(map(int, args["--args"].split(",")))  # type: ignore
    else:
        argv = []

    # debug=True will make print cannot work in ti.func
    ti.init(
        arch=ti.gpu,
        excepthook=True,
        advanced_optimization=(not args["--debug"]),
        verbose=args["--verbose"],
    )
    # }}} Parse #

    # pixels and paint must be defined in a same file
    if args["<command>"] in ["line"]:
        from . import init, pixels

        if args["--second"]:
            from .line.bresenham import paint
        else:
            from .line.midpoint import paint
        argv = argv if argv else [100, 5, 3, 3]
    elif args["<command>"] in ["circle"]:
        from . import init, pixels

        if args["--second"]:
            from .circle.bresenham import paint
        else:
            from .circle.midpoint import paint
        argv = argv if argv else [100, 50, 25]
    elif args["<command>"] in ["ellipse"]:
        from . import init, pixels
        from .ellipse import paint

        argv = argv if argv else [100, 50, 30, 10]
    elif args["<command>"] in ["fill"]:
        from . import init, pixels

        if args["--second"]:
            from .fill.seed import paint

            argv = argv if argv else [50, 30, 0, 0, 100, 50, 25, 100]
        else:
            from .fill.scan import paint

            argv = argv if argv else [0, 0, 100, 50, 50, 30, 25, 100]

    elif args["<command>"] in ["bezier"]:
        from . import init, pixels
        from .bezier import paint

        argv = argv if argv else [100, 0, 0, 30, 300, 300, 300]
    elif args["<command>"] in ["b"]:
        from . import init, pixels
        from .b import paint

        argv = (
            argv
            if argv
            else [
                3,
                0,
                0,
                100,
                300,
                200,
                100,
                300,
                300,
                400,
                100,
                500,
                400,
                600,
                0,
                700,
                500,
            ]
        )
    elif args["<command>"] in ["koch"]:
        from . import init, pixels
        from .koch import paint

        argv = argv if argv else [4, 5, 0, 0]
    elif args["<command>"] in ["mandelbrot"]:
        from . import init, pixels
        from .mandelbrot import paint

        argv = argv if argv else [2, 20]
    elif args["<command>"] in ["julia"]:
        from . import init, pixels
        from .julia import paint

        argv = argv if argv else [2, 20]
    elif args["<command>"] in ["fern"]:
        from . import init, pixels
        from .fern import paint

        argv = argv if argv else [50, 2000, 512, 0]
    elif args["<command>"] in ["reality"]:
        from . import pixels
        from .reality import paint, init, spheres

        ti.root.dense(ti.i, 20).place(spheres)
        argv = argv if argv else [4, 0.05]
    else:
        _name = os.path.split(__file__)[-1]
        exit(f"{args['<command>']} is an illegal command. See '{_name} -h'.")

    if args["--verbose"]:
        print(argv)

    out: Optional[str] = args["--output"]  # type: ignore
    if not out:
        out = ""
    ext = out.split(".")[-1]
    output_dir = os.path.split(out)[0]
    if output_dir == "":
        output_dir = "."
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if ext in ["mp4", "gif"]:
        video_manager = ti.VideoManager(
            output_dir=output_dir, automatic_build=False
        )
    elif ext in ["png", "jpg", "bmp"]:
        i = 0

    shape = (int(args["--width"]), int(args["--height"]))  # type: ignore
    ti.root.dense(ti.ij, shape).place(pixels)
    init()
    gui = ti.GUI(args["<command>"], shape)
    import time

    timeout = float(args["--timeout"])  # type: ignore
    start = time.time()
    while time.time() - start < timeout and gui.running:
        paint(R, G, B, *argv)
        if not args["--dry-run"]:
            gui.set_image(pixels)
            gui.show()
        if ext in ["mp4", "gif"]:
            video_manager.write_frame(pixels)  # type: ignore
        elif ext in ["png", "jpg", "bmp"]:
            i += 1  # type: ignore
            try:
                file = out % i
            except TypeError:
                file = out
            ti.imwrite(pixels, file)

    if ext == "mp4":
        video_manager.make_video(gif=False)  # type: ignore
    if ext == "gif":
        video_manager.make_video(mp4=False)  # type: ignore


if __name__ == "__main__" and __doc__:
    main(__doc__)
# ex: foldmethod=marker
