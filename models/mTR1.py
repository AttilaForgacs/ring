import __builtin__
from models import BaseModel
from sympy import Symbol, solve
import sympy
from tools import *
from tools import _2_circles_tangential_equations

import matplotlib
from matplotlib import pyplot


class TR1(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR1, self).__init__(params, context)
        self.context = context
        self.params = params
        c = context
        c['slope_length'] = params.R20
        c['lc_R'] = params.R41
        c['lc_X'] = params.R41
        c['lc_Y'] = params.RI + params.H - params.R41

        c['rc_R'] = params.R41
        c['rc_X'] = params.W - params.R41
        c['rc_Y'] = params.RI + params.H - params.R41

        c['p1_X'] = params.R41
        c['p1_Y'] = params.RI + params.H

        c['p2_X'] = params.W - params.R41
        c['p2_Y'] = params.RI + params.H

        c['slope_base'] = sqrt((c['slope_length'] ** 2) / 2.)

        c['p3_X'] = c['slope_base']
        c['p3_Y'] = params.RI

        c['p4_X'] = 0
        c['p4_Y'] = params.RI + c['slope_base']

        c['p5_X'] = params.W - c['slope_base']
        c['p5_Y'] = params.RI

        c['p6_X'] = params.W
        c['p6_Y'] = params.RI + c['slope_base']

    def calculate_intersections(self):
        pass

    def solve(self):
        pass

    def get_volume(self):
        vars = self.context.variables
        c = self.context
        p = self.params

        ratio = ((p.W) / (p.H))
        pyplot.figure(1, figsize=(20, 20. * ratio))
        pyplot.gca().set_xlim(-1, p.W + 1)
        pyplot.gca().set_ylim(p.RI - 1, (p.RI + p.H + 1))
        pyplot.gca().set_aspect('equal')

        self.arctop = volume_integrate_arc_top(P(c['lc_X'], c['lc_Y']),
                                          c['lc_R'], a=0, b=c['p1_X']
        )
        self.linetop = volume_integrate_line(c['p1_Y'], a=c['p1_X'], b=c['p2_X'])
        self.arctop2 = volume_integrate_arc_top(P(c['rc_X'], c['rc_Y']), c['rc_R'],
                                           a=c['p2_X'], b=p.W)

        top = sum([self.arctop, self.linetop, self.arctop2])

        self.bottom_slope = volume_integrate_slope(c['p4_X'], c['p4_Y'],
                                              c['p3_X'], c['p3_Y'],
                                              a=0., b=c['p3_X'])
        self.bottom_line = volume_integrate_line(p.RI, c['p3_X'], c['p5_X'])
        self.bottom_slope2 = volume_integrate_slope(c['p5_X'], c['p5_Y'],
                                               c['p6_X'], c['p6_Y'],
                                               a=c['p5_X'], b=p.W)

        bottom = sum([self.bottom_slope, self.bottom_line, self.bottom_slope2])
        volume = top - bottom
        return float(volume / 1000.)