#! /usr/bin/env bash
#? 0.0.1
##? Generate images of README.md.
##?
##? usage: generate_images.bash [options]
##?
##? options:
##?   -h, --help            Show this screen.
##?   -V, --version         Show version.
help=$(grep "^##?" "$0" | cut -c 5-)
version=$(grep "^#?" "$0" | cut -c 4-)
eval "$(docopts -h "$help" -V "$version" : "$@")"
[ -d images ] || mkdir images
[ -x cg.py ] && parallel ./cg.py -nt1 -oimages/{}.png {} ::: \
  line \
  circle \
  ellipse \
  fill \
  bezier \
  b \
  koch \
  mandelbrot \
  julia \
  fern \
  reality
[ -x cg.py ] && ./cg.py -oimages/16line.png \
  -a512,256,612,256,512,256,612,306,512,256,612,356,512,256,552,356,512,256,512,356,512,256,462,356,512,256,412,356,512,256,412,306,512,256,412,256,512,256,412,206,512,256,412,156,512,256,462,156,512,256,512,156,512,256,552,156,512,256,612,156,512,256,612,206 line
