#coding: utf-8
import csv
from pylab import *
from collections import *
from scipy.integrate import quad
from math import *
from collections import *
#degrees = 180 * radians / pi
#radians = pi * degrees / 180
from config import RING_PROFILES_DB_PATH
from sympy import *

P = namedtuple('Point', ['x', 'y']);

INTEGRATE_STEP = 0.001
EPS = 1e-5  #epsilon for error checking


def test_eq(a, b):
    assert abs(a - b) <= EPS


def vector_length(pa, pb):
    return sqrt((pa.x - pb.x) ** 2 + (pa.y - pb.y) ** 2)


def get_angle_between_3_points(pc, p1, p2):
    """ pc=point center, p1,p2 """
    vl = vector_length
    return arccos(
        ( vl(pc, p1) ** 2 + vl(pc, p2) ** 2 - vl(p1, p2) ** 2 ) / (
            2 * vl(pc, p1) * vl(pc, p2)))


def f_line(x, h):
    return h


def f_slope(x, x1, y1, x2, y2):
    """
    y = y1 + [(y2 - y1) / (x2 - x1)]·(x - x1)
    """
    return y1 + ( (y2 - y1) / (x2 - x1) ) * (x - x1)


def f_top_arc(x, C, r):
    """ @param x independent var
        @param C circle mid point
        @param r radius
    """
    try:
        y = C.y + ( sqrt(r ** 2 - (x - C.x) ** 2) )
    except:
        y = 0.
    return y


f_bottom_arc = lambda x, C, r: (C.y - ( sqrt(r ** 2 - (x - C.x) ** 2) ))


def integrate_arc_top(C, r, a, b):
    return quad(lambda z: f_top_arc(z, C, r), a, b)[0]


def integrate_arc_bottom(C, r, a, b):
    return quad(lambda z: f_bottom_arc(z, C, r), a, b)[0]


def integrate_line(h, a, b):
    return quad(lambda z: f_line(z, h), a, b)[0]


def integrate_slope(x1, y1, x2, y2, a, b):
    return quad(lambda z: f_slope(z, x1, y1, x2, y2), a, b)[0]


def volume_integrate_arc_top(C, r, a, b):
    rng = arange(a, b, INTEGRATE_STEP)
    #plot(rng, map(lambda z: f_top_arc(z, C, r), rng))
    return pi * ( quad(lambda z: (f_top_arc(z, C, r) ** 2), a, b)[0] )


def volume_integrate_arc_bottom(C, r, a, b):
    rng = arange(a, b, INTEGRATE_STEP)
    #plot(rng, map(lambda z: f_bottom_arc(z, C, r), rng))
    return pi * ( quad(lambda z: (f_bottom_arc(z, C, r) ** 2), a, b)[0] )


def volume_integrate_line(h, a, b):
    rng = arange(a, b, INTEGRATE_STEP)
    #plot(rng, map(lambda z: f_line(z, h), rng))
    return pi * ( quad(lambda z: (f_line(z, h) ** 2), a, b)[0] )


def volume_integrate_slope(x1, y1, x2, y2, a, b):
    rng = arange(a, b, INTEGRATE_STEP)
    #plot(rng, map(lambda z: f_slope(z, x1, y1, x2, y2), rng))
    return pi * ( quad(lambda z: (f_slope(z, x1, y1, x2, y2) ** 2), a, b)[0] )


def vol_sphere(r):
    return (4. / 3.) * pi * (r ** 3)


def _2_circles_tangential_equations(c1, c2, var_name, variables_list, context):
    '''
    c1: string name of circle 1
    c2: string name of other circle
    var_name: string, independent will be created
    '''
    G = context
    c1_CX = G['{}_CX'.format(c1)]
    c1_CY = G['{}_CY'.format(c1)]
    c1_R = G['{}_R'.format(c1)]

    c2_CX = G['{}_CX'.format(c2)]
    c2_CY = G['{}_CY'.format(c2)]
    c2_R = G['{}_R'.format(c2)]
    X = Symbol(var_name + '_X')
    Y = Symbol(var_name + '_Y')
    variables_list += [X, Y]
    eq_c1 = (X - c1_CX) ** 2 + (Y - c1_CY) ** 2 - c1_R ** 2
    eq_c2 = (X - c2_CX) ** 2 + (Y - c2_CY) ** 2 - c2_R ** 2
    eq_line = (Y - c2_CY) * (c1_CX - c2_CX) - (X - c2_CX) * (c1_CY - c2_CY)
    return [eq_c1, eq_c2, eq_line]


class RingParams(object):
    def __str__(self):
        return 'PR={} MDL={} W={} H={}'.format(
            self.PROFILE,
            self.MODEL,
            self.W,
            self.H
        )

    def __init__(self, W=0, H=0, CF=0, PROFILE=''):
        super(RingParams, self).__init__()
        #known in advance
        self.W = W
        self.H = H
        self.CF = CF
        self.PROFILE = PROFILE
        #calculated
        self.RI = CF / 2. * pi
        self.RI = round(self.RI, 5)
        #looked up
        self.MODEL = None
        self.R60 = None
        self.R61 = None
        self.R20 = None
        self.R40 = None
        self.R41 = None

    def lookup_definition(self, ctx):
        mapping = ctx[self.PROFILE]
        self.MODEL = mapping['TR_CODE']
        self.R60 = float(mapping['R60'] or 0.)
        self.R61 = float(mapping['R61'] or 0.)
        self.R20 = float(mapping['R20'] or 0.)
        self.R40 = float(mapping['R40'] or 0.)
        self.R41 = float(mapping['R41'] or 0.)


def load_profiles_lookup_table(ctx):
    with open(RING_PROFILES_DB_PATH) as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        reader.next()
        for row in reader:
            PR_CODE = row[0]
            r = ctx[PR_CODE] = {}
            r['TR_CODE'] = row[1]
            r['PROFIL_CODE'] = row[2]
            r['H'] = row[3]
            r['W'] = row[4]
            r['R60'] = row[5]
            r['R61'] = row[6]
            r['R20'] = row[7]
            r['R40'] = row[8]
            r['R41'] = row[9]
            r['P1'] = row[10]
            r['P2'] = row[11]
            r['P3'] = row[12]
            r['P4'] = row[13]
            r['BESCHREIBUNG'] = row[14]
    return ctx


class Context(dict):
    def __init__(self):
        super(Context, self).__init__()
        self.variables = []
        self.equations = []