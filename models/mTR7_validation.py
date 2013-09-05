import __builtin__
from operator import itemgetter
from models import BaseModel
from sympy import Symbol, solve
import sympy
from tools import *
from tools import _2_circles_tangential_equations


class TR7(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR7, self).__init__(params, context)
        self.context = context
        self.params = params
        c = context

        c['bbc_R'] = params.R61
        c['btc_R'] = params.R60

        c['bbc_CX'] = params.W / 2.
        c['bbc_CY'] = params.RI + c['bbc_R']

        c['btc_CX'] = params.W / 2.
        c['btc_CY'] = params.RI + params.H - c['btc_R']

        c['lsc_R'] = params.R40
        c['lsc_CX'] = params.R40
        c['lsc_CY'] = mkSymbol('lsc_CY')

        c['rsc_R'] = params.R40
        c['rsc_CX'] = params.W - params.R40
        c['rsc_CY'] = mkSymbol('rsc_CY')

    def calculate_intersections(self):
        super(TR7, self).calculate_intersections()

        c = self.context
        p = self.params

        c.equations = []
        c.variables = [c['lsc_CY']]
        c.equations += _2_circles_tangential_equations('lsc', 'btc', 'p1',
                                                       c.variables, c)

        self.s_1_all = sympy.solve(c.equations, *c.variables, dict=True)
        self.s_1_fil = (
            sorted(self.s_1_all, key=itemgetter(c['lsc_CY']),
                   reverse=False)[2]
        )

        c.equations = []
        c.variables = [c['lsc_CY']]
        c.equations += _2_circles_tangential_equations('lsc', 'bbc', 'p3',
                                                       c.variables, c)

        self.s_2_all = sympy.solve(c.equations, *c.variables, dict=True)
        self.s_2_fil = (
            sorted(self.s_2_all, key=itemgetter(c['lsc_CY']),
                   reverse=True)[2]
        )

        c['p1_X'] = self.s_1_fil[c['p1_X']]
        c['p1_Y'] = self.s_1_fil[c['p1_Y']]

        c['p2_Y'] = c['p1_Y']
        c['p2_X'] = p.W - c['p1_X']

        c['p3_X'] = self.s_2_fil[c['p3_X']]
        c['p3_Y'] = self.s_2_fil[c['p3_Y']]

        c['p4_Y'] = c['p3_Y']
        c['p4_X'] = p.W - c['p3_X']

        c['rsc_CY'] = c['lsc_CY'] = self.s_1_fil[c['lsc_CY']]

    def solve(self):
        pass

    def get_volume(self):
        vars = self.context.variables
        c = self.context
        p = self.params

        top = __builtin__.sum([
            volume_integrate_arc_top(
                P(c['lsc_CX'], c['lsc_CY']),
                c['lsc_R'],
                0., c['p1_X']),

            volume_integrate_arc_top(
                P(c['btc_CX'], c['btc_CY']), c['btc_R'],
                c['p1_X'], c['p2_X']),

            volume_integrate_arc_top(P(c['rsc_CX'], c['rsc_CY']),
                                     c['rsc_R'],
                                     c['p2_X'], p.W)
        ])

        bottom = __builtin__.sum([
            volume_integrate_arc_bottom(P(c['lsc_CX'],
                                          c['lsc_CY']), c['lsc_R'],
                                        0.,
                                        c['p3_X']),
            volume_integrate_arc_bottom(P(c['bbc_CX'], c['bbc_CY']),
                                        c['bbc_R'],
                                        c['p3_X'], c['p4_X']),

            volume_integrate_arc_bottom(
                P(c['rsc_CX'], c['rsc_CY']),
                c['rsc_R'],
                c['p4_X'], p.W),
        ])

        volume = top - bottom
        return float(volume / 1000.)
