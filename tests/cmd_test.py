"""Test cmd."""

import shlex
import subprocess


class Test:
    """Test."""

    def test_help(self):
        """Test --help."""

        cmd = "cgdemo --help"
        args = shlex.split(cmd)
        out = subprocess.run(args, capture_output=True).stdout.decode()
        expect = """\
Computer graphics algorithms demonstration.

usage: cgdemo [-hVdns] [ [-v] | [-q|-qq] ] [-x <height>] [-y <width>]
    [-o <out>] [-c <color>] [-a <args>] [-t <time>] <command>

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

Report bugs to <wuzy01@qq.com>.
"""
        assert out == expect
