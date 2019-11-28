

"""
Copyright 2011 Tyler Kennedy <tk@tkte.ch>. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY TYLER KENNEDY ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from itertools import product
from math import atan2, cos, hypot, pi

import Image

def translate_coords(source, theta, zoom):
    """
    Translate a 3D coordinate around an imaginary 3D carousel, returning a 2D
    coordinate.

    This function is meant to fake camera and modelview matrix translations in
    a cheap yet convincing manner.
    """

    ORIGINX = 5
    ORIGINY = 5
    # ORIGINZ is trivially zero and the maths are simplified around this.

    x, y, z = source
    x -= ORIGINX
    y -= ORIGINY

    # Get the carousel. The carousel is a circle which the coordinate is
    # rotated around during transformation; it is sufficient to merely find
    # the radius of the carousel, since the origin is used as the center.
    carousel = hypot(x, z)

    # Get the current offset angle. This is the angle which the coordinate is
    # currently located at on the carousel.
    offset = atan2(z, x)

    # Get the new X coordinate.
    x = cos(theta + offset) * carousel

    return int((x + ORIGINX) * zoom), int((y + ORIGINY) * zoom)

# The sections of the skin, as source coords on the skin and untransformed
# dest coords. Always wind coordinates CCW.
lefts = [
    (False, (16, 8, 24, 16),
     ((4, 1, 1.5), (4, 3, 1.5), (4, 3, -0.5), (4, 1, -0.5))), # Head (left)
    (False, (8, 20, 12, 32),
     ((4, 6, 1), (4, 9, 1), (4, 9, 0), (4, 6, 0))), # Leg (left)
    (False, (48, 20, 52, 32),
     ((3, 3, 1), (3, 6, 1), (3, 6, 0), (3, 3, 0))), # Arm (left)
    (True, (32, 8 ,40, 16),
     ((3.875, 0.875, 1.625), (3.875, 3.125, 1.625),
      (3.875, 3.125, -0.625), (3.875, 0.875, -0.625))), # Accessory (left)
]
rights = [
    (False, (0, 8, 8, 16),
     ((6, 1, -0.5), (6, 3, -0.5), (6, 3, 1.5), (6, 1, 1.5))), # Head (right)
    (False, (0, 20, 4, 32),
     ((6, 6, 0), (6, 9, 0), (6, 9, 1), (6, 6, 1))), # Leg (right)
    (False, (40, 20, 44, 32),
     ((7, 3, 0), (7, 6, 0), (7, 6, 1), (7, 3, 1))), # Arm (right)
    (True, (48, 8 ,56, 16),
     ((5.875, 0.875, -0.625), (5.875, 3.125, -0.625),
      (5.875, 3.125, 1.625), (5.875, 0.875, 1.625))), # Accessory (left)
]
fronts = [
    (False, (8, 8, 16, 16),
     ((4, 1, 1.5), (4, 3, 1.5), (6, 3, 1.5), (6, 1, 1.5))), # Head (front)
    (False, (4, 20, 8, 32),
     ((4, 6, 1), (4, 9, 1), (5, 9, 1), (5, 6, 1))), # Leg (front) (right)
    (False, (4, 20, 8, 32),
     ((5, 6, 1), (5, 9, 1), (6, 9, 1), (6, 6, 1))), # Leg (front) (left)
    (False, (20, 20, 28, 32),
     ((4, 3, 1), (4, 6, 1), (6, 6, 1), (6, 3, 1))), # Body (front)
    (False, (44, 20, 48, 32),
     ((3, 3, 1), (3, 6, 1), (4, 6, 1), (4, 3, 1))), # Arm (front) (left)
    (False, (44, 20, 48, 32),
     ((6, 3, 1), (6, 6, 1), (7, 6, 1), (7, 3, 1))), # Arm (front) (right)
    (True, (40, 8, 48, 16),
     ((3.875, 0.875, 1.625), (3.875, 3.125, 1.625),
      (6.125, 3.125, 1.625), (6.125, 0.875, 1.625))), # Accessory (front)
]
backs = [
    (False, (24, 8, 32, 16),
     ((6, 1, -0.5), (6, 3, -0.5), (4, 3, -0.5), (4, 1, -0.5))), # Head (back)
    (False, (12, 20, 16, 32),
     ((5, 6, 0), (5, 9, 0), (4, 9, 0), (4, 6, 0))), # Leg (back) (right)
    (False, (12, 20, 16, 32),
     ((6, 6, 0), (6, 9, 0), (5, 9, 0), (5, 6, 0))), # Leg (back) (left)
    (False, (32, 20, 40, 32),
     ((6, 3, 0), (6, 6, 0), (4, 6, 0), (4, 3, 0))), # Body (back)
    (False, (52, 20, 56, 32),
     ((4, 3, 0), (4, 6, 0), (3, 6, 0), (3, 3, 0))), # Arm (back) (left)
    (False, (52, 20, 56, 32),
     ((7, 3, 0), (7, 6, 0), (6, 6, 0), (6, 3, 0))), # Arm (back) (right)
    (True, (56, 8, 64, 16),
     ((3.875, 0.875, -0.625), (3.875, 3.125, -0.625),
      (6.125, 3.125, -0.625), (6.125, 0.875, -0.625))), # Accessory (back)
]
edges = [
]

def render_skin(skin, theta, zoom):
    """
    Take a skin, and render it, enlarged, with a perspective.
    """

    size = (10 * zoom, 10 * zoom)

    colorkey = skin.getpixel((63, 0))[0:3]

    out = Image.new("RGBA", size, (0, 0, 0, 0))

    # Constrain theta, and figure out which sections we're gonna draw.
    theta %= 2 * pi
    if 0 <= theta < pi / 2:
        sections = [edges, fronts, rights]
    elif theta < pi:
        sections = [edges, backs, rights]
    elif theta < 3 * pi / 2:
        sections = [edges, backs, lefts]
    else:
        sections = [edges, fronts, lefts]

    targets = []
    sources = []

    for section in sections:
        for trans, source, dest in section:
            transformed = [translate_coords(i, theta, zoom) for i in dest]
            xs, ys = zip(*transformed)
            l = min(xs)
            r = max(xs)
            u = min(ys)
            d = max(ys)
            # Discard unviewable slices. They'll cause exceptions and won't
            # even show up anyway.
            if l == r or u == d:
                continue

            targets.append((l, u, r, d))
            l, u, r, d = source
            sources.append((l, u, l, d, r, d, r, u))
            if trans:
                pbo = skin.load()
                for coords in product(xrange(l, r), xrange(u, d)):
                    rgb = pbo[coords][0:3]
                    if rgb == colorkey:
                        pbo[coords] = (42, 42, 42, 0)

    for target, source in zip(targets, sources):
        w = target[2] - target[0]
        h = target[3] - target[1]
        temp = skin.transform((w, h), Image.QUAD, source)
        out.paste(temp, target, temp)

    return out

def main(skinfile):
    """
    Render a three-quarters view of a skin.

    This can be scaled up by any factor; the minimal coordinates are 10x10.
    """

    FACTOR = 32
    BG = (240, 240, 240, 255)

    skin = Image.open(skinfile).convert("RGBA")

    for i in range(0, 360, 6):
        #print "Making image %d" % i
        theta = i * 2 * pi / 360
        out = render_skin(skin, theta, FACTOR)
        temp = Image.new("RGBA", out.size, BG)
        out = Image.composite(out, temp, out)
        out.save("test%03d.gif" % i)

if __name__ == "__main__":
    import sys
    main(sys.argv[-1])
