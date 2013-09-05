import __builtin__
from models import BaseModel
from tools import *
from tools import _2_circles_tangential_equations, _2_circles_tangential_equations_constrained
from operator import itemgetter
import numpy as np
import solver


class TR2(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR2, self).__init__(params, context)

        self.context = context
        self.params = params
        c = context
        p = params

        c['tc_R'] = p.R61
        c['tc_CX'] = p.W / 2.
        c['tc_CY'] = p.RI + p.H - p.R61

        c['lc_R'] = p.R41
        c['lc_CX'] = p.R41
        c['lc_CY'] = None

        c['rc_R'] = p.R41
        c['rc_CX'] = p.W - p.R41
        c['rc_CY'] = None # later


    def calculate_intersections(self):
        super(TR2, self).calculate_intersections()

        c = self.context
        p = self.params

        c.variables = []
        c.equations = []

        solutions = solver.calc_intersection('tc', 'lc', c)

        self.sub_result = (
            sorted(solutions, key=itemgetter(2), reverse=True)[1]
        )

        x = float(self.sub_result[0])
        y = float(self.sub_result[1])
        cy = float(self.sub_result[2])

        c['p1_X'] = x
        c['p1_Y'] = y

        c['p2_Y'] = y
        c['p2_X'] = p.W - x

        c['lc_CY'] = cy
        c['rc_CY'] = cy

    def get_volume(self):
        c = self.context
        p = self.params

        a = p.R20 / (2 ** 0.5)

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

        abottom1, bh1 = volume_integrate_slope_bottom(
            0., p.RI + a,
            a, p.RI,
            0., a
        )

        aline, bh2 = volume_integrate_line(
            h=p.RI,
            a=a,
            b=p.W - a
        )

        abottom2, bh3 = volume_integrate_slope_bottom(
            p.W - a, p.RI,
            p.W, p.RI + a,
            p.W - a, p.W
        )

        bottom = sum([abottom1, aline, abottom2])

        volume = top - bottom
        min_height = min_drop_nones(th1, th2, th3) - max_drop_nones(bh1, bh2,
                                                                    bh3)

        return (
            float(volume / 1000.),
            min_height
        )