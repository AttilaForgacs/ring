import __builtin__
from models import BaseModel
from sympy import Symbol, solve
from tools import _2_circles_tangential_equations, volume_integrate_arc_top, volume_integrate_arc_bottom, P


class TR7(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR7, self).__init__(params, context)
        self.context = context
        self.params = params
        c = context
        c['bbc_R'] = params.R60
        c['btc_R'] = params.R61
        c['bbc_CX'] = params.W / 2.
        c['bbc_CY'] = params.RI + c['bbc_R']
        c['btc_CX'] = params.W / 2.
        c['btc_CY'] = params.RI + params.H - c['btc_R']
        c['lsc_R'] = Symbol('lsc_R', positive=True)
        c['lsc_CX'] = Symbol('lsc_CX')
        c['lsc_CY'] = Symbol('lsc_CY')
        c['rsc_R'] = Symbol('rsc_R', positive=True)
        c['rsc_CX'] = Symbol('rsc_CX')
        c['rsc_CY'] = Symbol('rsc_CY')

    def create_equations(self):
        super(TR7, self).create_equations()

        c = self.context
        p = self.params

        c.variables = [
            c['lsc_CX'],
            c['lsc_CY'],
            c['lsc_R'],
            c['rsc_CX'],
            c['rsc_CY'],
            c['rsc_R'],
        ]

        c.equations += [c['lsc_CX'] - c['lsc_R']]
        c.equations += [c['rsc_CX'] - p.W + c['rsc_R']]

        c.equations += _2_circles_tangential_equations('lsc', 'btc', 'p1',
                                                       c.variables, c)
        c.equations += _2_circles_tangential_equations('lsc', 'bbc', 'p3',
                                                       c.variables, c)
        c.equations += _2_circles_tangential_equations('rsc', 'btc', 'p2',
                                                       c.variables, c)
        c.equations += _2_circles_tangential_equations('rsc', 'bbc', 'p4',
                                                       c.variables, c)

    def solve(self):
        super(TR7, self).start()
        c = self.context
        p = self.params
        solutions = solve(c.equations, *c.variables, dict=True)
        super(TR7, self).stop()
        filtered_solutions = [s for s in solutions
                              if
                              p.RI + p.H > s[c['lsc_CY']] > p.RI and
                              p.RI + p.H > s[c['rsc_CY']] > p.RI
        ]
        self.solutions = filtered_solutions
        return filtered_solutions

    def get_volume(self):

        S = self.solutions[0]
        vars = self.context.variables
        c = self.context
        p = self.params

        import ipdb
        ipdb.set_trace()


        top = __builtin__.sum([
            volume_integrate_arc_top(P(S[c['lsc_CX']], S[c['lsc_CY']]),
                                     S[c['lsc_R']], 0.,
                                     S[Symbol('p1_X')]),

            volume_integrate_arc_top(P(c['btc_CX'], c['btc_CY']), c['btc_R'],
                                     S[Symbol('p1_X')], S[Symbol('p2_X')]),

            volume_integrate_arc_top(P(S[c['rsc_CX']], S[c['rsc_CY']]),
                                     S[c['rsc_R']],
                                     S[Symbol('p2_X')], p.W),
        ])

        bottom = __builtin__.sum([
            volume_integrate_arc_bottom(P(S[c['lsc_CX']],
                                          S[c['lsc_CY']]), S[c['lsc_R']],
                                        0.,
                                        S[Symbol('p3_X')]),
            volume_integrate_arc_bottom(P(c['bbc_CX'], c['bbc_CY']),
                                        c['bbc_R'],
                                        S[Symbol('p3_X')], S[Symbol('p4_X')]),
            volume_integrate_arc_bottom(
                P(S[c['rsc_CX']], S[c['rsc_CY']]),
                S[c['rsc_R']],
                S[Symbol('p4_X')], p.W),
        ])

        volume = top - bottom
        return float(volume / 1000.)