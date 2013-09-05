import __builtin__
from models import BaseModel
from sympy import Symbol, solve
import sympy
from tools import *
from tools import _2_circles_tangential_equations
from operator import itemgetter
import numpy as np
from matplotlib import pyplot


class TR13(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR13, self).__init__(params, context)
        self.context = context
        self.params = params
        c = context
        p = params

        c['p3_X'] = p.R40
        c['p3_Y'] = p.RI

        c['p4_X'] = p.W - p.R40
        c['p4_Y'] = p.RI

        c['tc_R'] = p.R61
        c['tc_CX'] = p.W / 2.
        c['tc_CY'] = p.RI + p.H - p.R61

        c['lc_R'] = p.R41
        c['lc_CX'] = p.R41
        c['lc_CY'] = mkSymbol('lc_CY')  #p.RI + p.R41

        c['rc_R'] = p.R41
        c['rc_CX'] = p.W - p.R41
        c['rc_CY'] = None # later

    def calculate_intersections(self):
        super(TR13, self).calculate_intersections()

        c = self.context
        p = self.params

        c.variables = [c['lc_CY']]

        c.equations = []
        c.equations += _2_circles_tangential_equations('lc', 'tc', 'p1',
                                                       c.variables, c)

        solutions = sympy.solve(c.equations, *c.variables, dict=True)

        # get the solution where circle is above(y) the other
        print 'solutions:', len(solutions)

        self.sub_result = (
            sorted(solutions, key=itemgetter(c['lc_CY']), reverse=True)[1]
        )

        c['p2_Y'] = self.sub_result[c['p1_Y']]
        c['p2_X'] = p.W - self.sub_result[c['p1_X']]
        c['p1_X'] = self.sub_result[c['p1_X']]
        c['p1_Y'] = self.sub_result[c['p1_Y']]
        c['rc_CY'] = self.sub_result[c['lc_CY']]
        c['lc_CY'] = self.sub_result[c['lc_CY']]

    def solve(self):
        pass

    def get_volume(self):
        vars = self.context.variables
        c = self.context
        p = self.params

        '''
                ratio = ((p.W) / (p.H))
                pyplot.figure(1, figsize=(20, 20. * ratio))
                pyplot.gca().set_xlim(-1, p.W + 1)
                pyplot.gca().set_ylim(p.RI - 1, (p.RI + p.H + 1))
                pyplot.gca().set_aspect('equal')
        '''

        atop1, th1 = volume_integrate_arc_top(
            P(c['lc_CX'], c['lc_CY']),
            c['lc_R'],
            0., c['p1_X']
        )

        atop2, th2 = volume_integrate_arc_top(
            P(c['tc_CX'], c['tc_CY']),
            c['tc_R'],
            c['p1_X'], c['p2_X']
        )

        atop3, th3 = volume_integrate_arc_top(
            P(c['rc_CX'], c['rc_CY']),
            c['rc_R'],
            c['p2_X'], p.W
        )

        top = sum([atop1, atop2, atop3])

        abottom1, bh1 = volume_integrate_arc_bottom(
            P(p.R40, p.RI + p.R40),
            p.R40,
            0., p.R40
        )

        aline, bh2 = volume_integrate_line(
            h=p.RI,
            a=p.R40,
            b=p.W - p.R40,
        )

        abottom2, bh3 = volume_integrate_arc_bottom(
            P(p.W - p.R40, p.RI + p.R40),
            p.R40,
            p.W - p.R40, p.W
        )

        bottom = sum([abottom1, aline, abottom2])

        volume = top - bottom
        min_height = min_drop_nones(th1, th2, th3) - max_drop_nones(bh1, bh2,
                                                                    bh3)

        return (
            float(volume / 1000.),
            min_height
        )