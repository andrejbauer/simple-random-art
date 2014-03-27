# -*- coding: utf-8 -*-

import Image
import op

def rgb(c):
    (r,g,b) = c
    return (int(127.5 * (r + 1.0)), int(127.5 * (g + 1.0)), int(127.5 * (b + 1.0)))

def makedata(width, height, f):
    sx = 2.0 / width
    sy = 2.0 / height
    for x in xrange(height):
        for y in xrange(width):
            yield rgb (f (sx * (x + 0.5) - 1.0, sy * (y + 0.5) - 1.0))

def compute(width, height, f):
    im = Image.new('RGB', (width, height))
    im.putdata(list(makedata(width, height, f)))
    return im

class RandomArt():
    def __init__(self, n=10, width=300, height=300):
        self.prog = op.Program(n)
        self.image = compute(width, height, self.prog.eval)
