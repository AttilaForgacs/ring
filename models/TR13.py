import __builtin__
from models import BaseModel
from sympy import Symbol, solve
import sympy
from tools import *
from tools import _2_circles_tangential_equations
from operator import itemgetter
from matplotlib import pyplot

#Hangs
class TR13(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR13, self).__init__(params, context)
        self.context = context
        self.params = params
        c = context
        p = params

        # c['lc_R'] = p.R41
        # c['lc_CX'] = p.R41
        # c['lc_CY'] = p.RI + p.R41
        #
        # c['rc_R'] = p.R40
        # c['rc_CX'] = p.W - p.R40
        # c['rc_CY'] = p.RI + p.R40

        c['p3_X'] = p.R41
        c['p3_Y'] = p.RI

        c['p4_X'] = p.W - p.R40
        c['p4_Y'] = p.RI

        c['tc_R'] = Symbol('tc_R', positive=True,real=True)
        c['tc_CX'] = Symbol('tc_CX', positive=True,real=True)
        c['tc_CY'] = Symbol('tc_CY', positive=True,real=True)

        c['lc_R'] = Symbol('lc_R', positive=True,real=True)
        c['lc_CX'] = Symbol('lc_CX', positive=True,real=True)
        c['lc_CY'] = Symbol('lc_CY', positive=True,real=True)

        c['rc_R'] = Symbol('rc_R', positive=True,real=True)
        c['rc_CX'] = Symbol('rc_CX', positive=True,real=True)
        c['rc_CY'] = Symbol('rc_CY', positive=True,real=True)

    def create_equations(self):
        super(TR13, self).create_equations()

        c = self.context
        p = self.params

        c.variables = [c['tc_CX'], c['tc_CY'], c['tc_R']]

        c.equations = []
        c.equations += _2_circles_tangential_equations('lc', 'tc', 'p1',
                                                       c.variables, c)
        c.equations += _2_circles_tangential_equations('rc', 'tc', 'p2',
                                                       c.variables, c)

        solutions = sympy.solve(c.equations, *c.variables, dict=True)
        # get the solution where circle is above(y) the other
        print 'solutions:', len(solutions)

        self.sub_result = (
            sorted(solutions, key=itemgetter(c['tc_CY']), reverse=True)[1]
        )

        c['tc_CX'] = self.sub_result[c['tc_CX']]
        c['tc_CY'] = self.sub_result[c['tc_CY']]
        c['tc_R'] = self.sub_result[c['tc_R']]


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

        abottom1 = volume_integrate_arc_bottom(
            P(c['lc_CX'], c['lc_CY']),
            c['lc_R'],
            0., c['p3_X']
        )

        aline = volume_integrate_line(
            h=p.RI,
            a=c['p3_X'],
            b=c['p4_X']
        )

        abottom2 = volume_integrate_arc_bottom(
            P(c['rc_CX'], c['rc_CY']),
            c['rc_R'],
            c['p4_X'], p.W
        )

        bottom = sum([abottom1, aline, abottom2])

        volume = top - bottom
        return float(volume / 1000.)



