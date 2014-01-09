import __builtin__
from models import BaseModel
from tools import *
from tools import _2_circles_tangential_equations, _2_circles_tangential_equations_constrained
from operator import itemgetter
import numpy as np
import solver


class TR170(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR170, self).__init__(params, context)

        self.context = context
        self.params = params
        c = context
        p = params

        c['tc_R'] = p.R61
        c['tc_CX'] = p.W / 2.
        c['tc_CY'] = p.RI + p.H - p.R61

        c['ltc_R'] = p.R41
        c['ltc_CX'] = p.R41
        c['ltc_CY'] = p.RI + p.R40

        c['lbc_R'] = p.P3
        c['lbc_CX'] = p.P3
        c['lbc_CY'] = p.RI + p.R40 - p.P2

        c['rtc_R'] = p.R41
        c['rtc_CX'] = p.W - p.R41
        c['rtc_CY'] = p.RI + p.R40

        c['rbc_R'] = p.R40
        c['rbc_CX'] = p.W - p.R40
        c['rbc_CY'] = p.RI + p.R40

    def calculate_intersections(self):
        super(TR170, self).calculate_intersections()

        c = self.context
        p = self.params

        c.variables = []
        c.equations = []

        solutions = solver.calc_intersection('ltc', 'tc', c)
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

        c['p3_X'] = p.P3
        #c['p3_Y'] = p.RI + p.R40 - p.P3
        c['p3_Y'] = c['lbc_CY'] - p.P3

        c['p4_X'] = p.W - p.R40 - p.P1
        c['p4_Y'] = p.RI

        c['p5_X'] = p.W - p.R40
        c['p5_Y'] = p.RI


    def get_volume(self):
        c = self.context
        p = self.params

        atop1, th1 = volume_integrate_arc_top(
            P(c['ltc_CX'], c['ltc_CY']),
            c['ltc_R'],
            0., c['p1_X']
        )

        atop2, th2 = volume_integrate_arc_top(
            P(c['tc_CX'], c['tc_CY']),
            c['tc_R'],
            c['p1_X'], c['p2_X']
        )

        atop3, th3 = volume_integrate_arc_top(
            P(c['rtc_CX'], c['rtc_CY']),
            c['rtc_R'],
            c['p2_X'], p.W
        )

        top = sum([atop1, atop2, atop3])

        abottom1, bh1 = volume_integrate_arc_bottom(
            P(c['lbc_CX'], c['lbc_CY']),
            c['lbc_R'],
            0., c['p3_X']
        )

        abottom2, bh2 = volume_integrate_slope_bottom(
            c['p3_X'], c['p3_Y'],
            c['p4_X'], c['p4_Y'],
            c['p3_X'], c['p4_X']
        )

        abottom3, bh3 = volume_integrate_slope_bottom(
            c['p4_X'], c['p4_Y'],
            c['p5_X'], c['p5_Y'],
            c['p4_X'], c['p5_X']
        )

        abottom4, bh4 = volume_integrate_arc_bottom(
            P(c['rbc_CX'], c['rbc_CY']),
            c['rbc_R'],
            c['p5_X'], p.W
        )

        bottom = sum([abottom1, abottom2, abottom3, abottom4])

        volume = top - bottom
        min_height = min_drop_nones(th1, th2, th3) - max_drop_nones(bh1, bh2,
                                                                    bh3, bh4)

        return (
            float(volume / 1000.),
            min_height
        )