import __builtin__
from models import BaseModel
from sympy import Symbol, solve
import sympy
from tools import *
from tools import _2_circles_tangential_equations
from operator import itemgetter
from matplotlib import pyplot
from sympy import Eq



#Hangs
class TR20(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR20, self).__init__(params, context)
        self.context = context
        self.params = params
        c = context
        p = params

        c['lc_R'] = p.R41
        c['lc_CX'] = p.R41
        c['lc_CY'] = p.RI + p.R41

        # was R40, assuming symmetry R40==R41
        c['rc_R'] = p.R41
        c['rc_CX'] = p.W - p.R41
        c['rc_CY'] = p.RI + p.R41

        c['tc_R'] = mkSymbol('tc_R')   #p.R61
        c['tc_CX'] = p.W / 2.
        c['tc_CY'] = mkSymbol('tc_CY')


    def create_equations(self):
        super(TR20, self).create_equations()

        c = self.context
        p = self.params

        c.variables = [c['tc_CY'], c['tc_R']]

        c.equations = [
            Eq(p.RI + p.H - c['tc_R'], c['tc_CY'])
        ]
        c.equations += _2_circles_tangential_equations('lc', 'tc', 'p1',
                                                       c.variables, c)

        solutions = sympy.solve(c.equations, *c.variables, dict=True)
        # get the solution where circle is above(y) the other
        print 'solutions:', len(solutions)

        self.sub_result = (
            sorted(solutions, key=itemgetter(c['tc_CY']), reverse=True)[1]
        )

        c['p1_X'] = self.sub_result[c['p1_X']]
        c['p1_Y'] = self.sub_result[c['p1_Y']]
        c['tc_R'] = self.sub_result[c['tc_R']]

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
        '''
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
        '''
        bottom = 0.
        volume = top - bottom
        return float(volume / 1000.)



