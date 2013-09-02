import __builtin__
from operator import itemgetter
from models import BaseModel
from sympy import Symbol, solve
import sympy
from tools import *
from tools import _2_circles_tangential_equations


class TR4(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR4, self).__init__(params, context)
        self.context = context
        self.params = params
        c = context

        # big top and bottom circles (R60/R61)
        c['bbc_R'] = params.R61
        c['btc_R'] = params.R60
        c['bbc_CX'] = params.W / 2.
        c['bbc_CY'] = params.RI + c['bbc_R']
        c['btc_CX'] = params.W / 2.
        c['btc_CY'] = params.RI + params.H - c['btc_R']

        # left top circle
        c['ltc_R'] = params.R41
        c['ltc_CX'] = params.R41
        c['ltc_CY'] = mkSymbol('ltc_CY')

        c['rtc_R'] = params.R41
        c['rtc_CX'] = params.W - params.R41
        c['rtc_CY'] = mkSymbol('rtc_CY')

        c['lbc_R'] = params.R40
        c['lbc_CX'] = params.R40
        c['lbc_CY'] = mkSymbol('lbc_CY')

        c['rbc_R'] = params.R40
        c['rbc_CX'] = params.W - params.R40
        c['rbc_CY'] = mkSymbol('rbc_CY')


    def create_equations(self):
        super(TR4, self).create_equations()

        c = self.context
        p = self.params


        #-------------------------------------------------------
        # 1
        #-------------------------------------------------------
        # c.equations = []
        # c.variables = [c['ltc_CY']]
        # c.equations += _2_circles_tangential_equations('ltc', 'btc', 'p1',
        #                                                c.variables, c)
        #
        # self.s_1_all = sympy.solve(c.equations, *c.variables, dict=True)
        #
        # self.s_1_fil = (
        #     sorted(self.s_1_all, key=itemgetter(c['ltc_CY']),
        #            reverse=False)[2]
        # )



        #-------------------------------------------------------
        # 2
        #-------------------------------------------------------
        c.equations = []
        c.variables = [c['lbc_CY']]
        c.equations += _2_circles_tangential_equations('lbc', 'bbc', 'p3',
                                                       c.variables, c)

        self.s_2_all = sympy.solve(c.equations, *c.variables, dict=True)
        self.s_2_fil = (
            sorted(self.s_2_all, key=itemgetter(c['lbc_CY']),
                   reverse=True)[2]
        )


        # substitution
        # c['p1_X'] = self.s_1_fil[c['p1_X']]
        # c['p1_Y'] = self.s_1_fil[c['p1_Y']]
        # c['p2_Y'] = c['p1_Y']
        # c['p2_X'] = p.W - c['p1_X']

        c['p3_X'] = self.s_2_fil[c['p3_X']]
        c['p3_Y'] = self.s_2_fil[c['p3_Y']]
        c['p4_Y'] = c['p3_Y']
        c['p4_X'] = p.W - c['p3_X']
        # c['rtc_CY'] = c['ltc_CY'] = self.s_1_fil[c['ltc_CY']]
        c['rbc_CY'] = c['lbc_CY'] = self.s_2_fil[c['lbc_CY']]


    def solve(self):
        pass

    def get_volume(self):
        vars = self.context.variables
        c = self.context
        p = self.params

        top = __builtin__.sum([

            # volume_integrate_arc_top(
            #     P(c['ltc_CX'], c['ltc_CY']),
            #     c['ltc_R'],
            #     0., c['p1_X']),

            # volume_integrate_arc_top(
            #     P(c['btc_CX'], c['btc_CY']), c['btc_R'],
            #     c['p1_X'], c['p2_X']),

            # volume_integrate_arc_top(P(c['rtc_CX'], c['rtc_CY']),
            #                          c['rtc_R'],
            #                          c['p2_X'], p.W)

            volume_integrate_arc_top(
                P(c['btc_CX'], c['btc_CY']), c['btc_R'],
                0., p.W),
        ])

        bottom = __builtin__.sum([
            volume_integrate_arc_bottom(P(c['lbc_CX'],
                                          c['lbc_CY']), c['lbc_R'],
                                        0.,
                                        c['p3_X']),
            volume_integrate_arc_bottom(P(c['bbc_CX'], c['bbc_CY']),
                                        c['bbc_R'],
                                        c['p3_X'], c['p4_X']),

            volume_integrate_arc_bottom(
                P(c['rbc_CX'], c['rbc_CY']),
                c['rbc_R'],
                c['p4_X'], p.W),
        ])

        volume = top - bottom
        return float(volume / 1000.)
