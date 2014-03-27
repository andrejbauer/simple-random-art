# The operators used by the random art generator

import math
import random

# Constants for the known types of data used by the operators
FLOAT = 'float'
POINT = 'point'
COLOR = 'color'

def distance(p1,p2):
    """The distance between points p1 and p2 in the plane."""
    (x1,y1) = p1
    (x2,y2) = p2
    return math.sqrt(2 * ((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))) * 0.5 - 1.0

def rgb_average(c1, c2, w):
    """Weighted average of two colors."""
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    v = 1.0 - w
    return (w*r1 + v*r2, w*g1 + v*g2, w*b1 + v*b2)

def average(x,y,w):
    """Weighted average of two numbers."""
    return w*x + (1-w)*y

def scale(x, a, b):
    return (x + 1.0) * 0.5 * (b - a) + a

### Operators

class Operator():
    """Each operator has the attributes name, args and ret:
       * name is the name to be displayed by __repr__
       * args is a list of types of the operator arguments
       * ret is the return type."""
    def __repr__(self):
        return self.name

class Faverage(Operator):
    name = 'faverage'
    args = (FLOAT, FLOAT)
    ret = FLOAT

    def __init__(self, scalars, foci, palette):
        self.w = scale(random.choice(scalars), 0.0, 1.0)

    def func(self, x, y):
        return average(x,y,self.w)

class Paverage(Operator):
    name = 'paverage'
    args = (POINT, POINT)
    ret = POINT

    def __init__(self, scalars, foci, palette):
        self.w1 = scale(random.choice(scalars), 0.0, 1.0)
        self.w2 = scale(random.choice(scalars), 0.0, 1.0)

    def func(self, p1, p2):
        (x1, y1) = p1
        (x2, y2) = p2
        return (average(x1,x2,self.w1), average(y1,y2,self.w2))


class Caverage(Operator):
    name = 'caverage'
    args = (COLOR, COLOR)
    ret = COLOR

    def __init__(self, scalars, foci, palette):
        self.w = scale(random.choice(scalars), 0.0, 1.0)

    def func(self, c1, c2):
        return rgb_average(c1, c2, self.w)

class RGB(Operator):
    name = 'rgb'
    args = (FLOAT, FLOAT, FLOAT)
    ret = COLOR

    def __init__(self, scalars, foci, palette):
        pass

    def func(self, r, g, b):
        return (r, g, b)

class Gray(Operator):
    name = 'rgb'
    args = (FLOAT,)
    ret = COLOR

    def __init__(self, scalars, foci, palette):
        pass

    def func(self, x):
        return (x, x, x)

class Distance(Operator):
    name = 'distance'
    args = (POINT,)
    ret = FLOAT

    def __init__(self, scalars, foci, palette):
        self.p = random.choice(foci)

    def func(self, q):
        return distance(q, self.p)

class Point(Operator):
    name = 'point'
    args = (FLOAT, FLOAT)
    ret = POINT

    def __init__(self, scalars, foci, palette):
        pass

    def func(self, x, y):
        return (x, y)

class ColorRing(Operator):
    name = 'colorring'
    args = (POINT,)
    ret = COLOR

    def __init__(self, scalars, foci, palette):
        (self.color1, self.color2) = random.sample(palette, 2)
        (r1, r2) = random.sample(scalars, 2)
        self.r1 = min(r1, r2) - 0.01
        self.r2 = max(r1, r2) + 0.01
        self.p = random.choice(foci)

    def func(self, q):
        d = distance(self.p, q)
        if d < self.r1: return self.color1
        elif d > self.r2: return self.color2
        else:
            w = (d - self.r1) / (self.r2 - self.r1)
            return rgb_average(self.color1, self.color2, w)

class Sin(Operator):
    name = 'sin'
    args = (FLOAT,)
    ret = FLOAT

    def __init__(self, scalars, foci, palette):
        self.x0 = random.choice(scalars)
        self.f = random.choice(scalars) * 10.0

    def func(self, x):
        return math.sin(self.f * x + self.x0)

class X(Operator):
    name = 'x'
    args = ()
    ret = FLOAT

    def __init__(self, scalars, foci, palette):
        self.x = None

    def func(self):
        return self.x

class Y(Operator):
    name = 'y'
    args = ()
    ret = FLOAT

    def __init__(self, scalars, foci, palette):
        self.y = None

    def func(self):
        return self.y

## The list of all operators used by the generation procedure.
## If you add a new operator, don't forget to include it here.
OPERATORS = (
    RGB, Gray, Point, ColorRing, Gray, Distance,
    Faverage, Paverage, Caverage,
    Sin
)

def random_rgb():
    return (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))

def random_float():
    return random.uniform(-1.0, 1.0)

def random_point():
    return (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))

def make_environment():
    scalars = [random_float() for i in xrange(random.randint(2,10))]
    foci = [random_point() for i in xrange(random.randint(2,10))]
    palette = [random_rgb() for i in xrange(random.randint(2,10))]
    return (scalars, foci, palette)

class Instruction():
    def __init__(self, addr, op, args):
        self.addr = addr
        self.op = op
        self.args = args
        self.used = False

    def __repr__(self):
        return '%d: %s %s' % (self.addr, self.op.name, self.args)

class Program():
    """The main generation procedure. The constructor takes
       a parameter which determines the size of the generated
       program, and optionally a list of operators.

       A program for drawing an image is represented by a
       list of instructions.
    """
    def __init__(self, n, operators=OPERATORS):
        (scalars, foci, palette) = make_environment()
        self.xop = X(scalars, foci, palette)
        self.yop = Y(scalars, foci, palette)
        prog = [Instruction(0, self.xop, []), Instruction(1, self.yop, [])]
        while len(prog) < n or prog[-1].op.ret != COLOR:
            (o,args) = Program.pick_and_connect(prog, operators)
            prog.append(Instruction(len(prog), o(scalars, foci, palette), args))
        # dead-code elimination
        Program.mark_used(len(prog)-1, prog)
        self.prog = prog
        opt = []
        remap = {}
        for (k,instr) in enumerate(prog):
            if instr.used:
                j = len(opt)
                instr.args = [remap[a] for a in instr.args]
                instr.addr = j
                remap[k] = j
                opt.append(instr)
        self.prog = opt
        self.memory = [None for i in range(len(opt))]
        self.code = [(instr.addr, instr.op.func, instr.args) for instr in self.prog]

    def eval(self, x, y):
        self.xop.x = x
        self.yop.y = y
        for (k, f, args) in self.code:
            self.memory[k] = f(*[self.memory[a] for a in args])
        return self.memory[-1]

    @staticmethod
    def pick_and_connect(prog, operators):
        connectible = []
        for op in operators:
            try:
                args = [random.choice([k for (k,instr) in enumerate(prog) if instr.op.ret==a])
                        for a in op.args]
                connectible.append((op, args))
            except IndexError:
                break                    
        return random.choice(connectible)

    @staticmethod
    def mark_used(k, prog):
        if not prog[k].used:
            prog[k].used = True
            for j in prog[k].args: Program.mark_used(j, prog)

    def __repr__(self):
        return '\n'.join(map(str,self.prog))
