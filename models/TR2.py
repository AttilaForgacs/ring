import __builtin__
from models import BaseModel
from sympy import Symbol, solve
import sympy
from tools import *
from tools import _2_circles_tangential_equations
from operator import itemgetter
from matplotlib import pyplot

class TR2(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR2, self).__init__(params, context)
        self.context = context
        self.params = params
        c = context
        p = params

        c['lc_R'] = params.R41
        c['lc_CX'] = params.R41
        c['lc_CY'] = Symbol('lc_CY', positive=True)

        c['tc_R'] = params.R61
        c['tc_CX'] = params.W / 2.
        c['tc_CY'] = params.RI + params.H - params.R61

        c['slope_length'] = params.R20

        # bottom begins here
        c['slope_base'] = sqrt((c['slope_length'] ** 2) / 2.)

        c['p3_X'] = 0.
        c['p3_Y'] = p.RI + c['slope_base']

        c['p4_X'] = c['slope_base']
        c['p4_Y'] = p.RI

        c['p5_X'] = p.W - c['slope_base']
        c['p5_Y'] = p.RI

        c['p6_X'] = p.W
        c['p6_Y'] = p.RI + c['slope_base']

    def create_equations(self):
        super(TR2, self).create_equations()

        c = self.context
        p = self.params

        c.variables = [c['lc_CY']]
        c.equations = []
        c.equations += _2_circles_tangential_equations('lc', 'tc', 'p1',
                                                       c.variables, c)
        solutions = sympy.solve(c.equations, *c.variables, dict=True)
        # get the solution where circle is above(y) the other

        self.sub_result = (
            sorted(solutions, key=itemgetter(c['lc_CY']), reverse=True)[1]
        )

        c['lc_CY'] = self.sub_result[c['lc_CY']]
        c['p1_X'] = self.sub_result[c['p1_X']]
        c['p1_Y'] = self.sub_result[c['p1_Y']]

        c['p2_X'] = p.W - c['p1_X']
        c['p2_Y'] = c['p1_Y']

        c['rc_R'] = c['lc_R']
        c['rc_CX'] = p.W - c['rc_R']
        c['rc_CY'] = c['lc_CY']



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


        atop1 = volume_integrate_arc_top(
            P(c['lc_CX'], c['lc_CY']),
            c['lc_R'],
            0., c['p1_X']
        )

        atop2 = volume_integrate_arc_top(
            P(c['tc_CX'], c['tc_CY']),
            c['tc_R'],
            c['p1_X'], c['p2_X']
        )

        atop3 = volume_integrate_arc_top(
            P(c['rc_CX'], c['rc_CY']),
            c['rc_R'],
            c['p2_X'], p.W
        )

        top = sum([atop1, atop2, atop3])

        bslope1 = volume_integrate_slope(
            c['p3_X'], c['p3_Y'],
            c['p4_X'], c['p4_Y'],
            0., c['p4_X']
        )

        bline1 = volume_integrate_line(p.RI, c['p4_X'], c['p5_X'])

        bslope2 = volume_integrate_slope(
            c['p5_X'], c['p5_Y'],
            c['p6_X'], c['p6_Y'],
            c['p5_X'], c['p6_X']
        )

        bottom = sum([bslope1, bline1, bslope2])

        volume = top - bottom
        return float(volume / 1000.)


