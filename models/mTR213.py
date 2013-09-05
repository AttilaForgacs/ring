import __builtin__
from models import BaseModel
from tools import *
from tools import _2_circles_tangential_equations, _2_circles_tangential_equations_constrained
from operator import itemgetter
import numpy as np
import solver
import math


class TR213(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR213, self).__init__(params, context)

        self.context = context
        self.params = params
        c = context
        p = params

        c['tc_R'] = p.R61
        c['tc_CX'] = p.W / 2.
        c['tc_CY'] = p.RI + p.H - p.R61

        c['bc_R'] = p.R60
        c['bc_CX'] = p.W / 2.
        c['bc_CY'] = p.RI + p.R60

        c['lbc_R'] = p.R40
        c['lbc_CX'] = p.R40
        c['lbc_CY'] = None

        c['rbc_R'] = p.R40
        c['rbc_CX'] = p.W - p.R40
        c['rbc_CY'] = None


    def calculate_intersections(self):
        super(TR213, self).calculate_intersections()

        c = self.context
        p = self.params
        c.variables = []
        c.equations = []

        c['x0'] = x0 = 0.
        c['y0'] = y0 = p.RI + p.H - p.P1 #P1==Hohe Sctrigbha, P2==Winkel

        x2 = x0 + math.cos(math.radians(90. - p.P2))
        y2 = y0 + math.sin(math.radians(90. - p.P2))

        solutions = solver.calc_line_vs_circle_intersections(
            'tc',
            x0, y0,
            x2, y2,
            c
        )
        self.sub_result = (
            sorted(solutions, key=itemgetter(1), reverse=True)[0]
        )

        x = float(self.sub_result[0])
        y = float(self.sub_result[1])

        c['x2'] = x
        c['y2'] = y

        solutions = solver.calc_intersection('bc', 'lbc', c)
        self.sub_result = (
            sorted(solutions, key=itemgetter(2), reverse=True)[-2]
        )

        x = float(self.sub_result[0])
        y = float(self.sub_result[1])
        cy = float(self.sub_result[2])

        c['p3_X'] = x
        c['p3_Y'] = y

        c['p4_Y'] = y
        c['p4_X'] = p.W - x

        c['lbc_CY'] = cy
        c['rbc_CY'] = cy

    def get_volume(self):
        c = self.context
        p = self.params

        atop1, th1 = volume_integrate_slope_top(
            c['x0'], c['y0'],
            c['x2'], c['y2'],
            0., c['x2']
        )

        atop2, th2 = volume_integrate_arc_top(
            P(c['tc_CX'], c['tc_CY']),
            c['tc_R'],
            c['x2'], p.W - c['x2']
        )

        atop3, th3 = volume_integrate_slope_top(
            p.W - c['x2'], c['y2'],
            p.W, c['y0'],
            p.W - c['x2'], p.W
        )

        top = sum([atop1, atop2, atop3])

        abottom1, bh1 = volume_integrate_arc_bottom(
            P(c['lbc_CX'], c['lbc_CY']),
            c['lbc_R'],
            0., c['p3_X']
        )

        aline, bh2 = volume_integrate_arc_bottom(
            P(c['bc_CX'], c['bc_CY']),
            c['bc_R'],
            c['p3_X'], c['p4_X']
        )

        abottom2, bh3 = volume_integrate_arc_bottom(
            P(c['rbc_CX'], c['rbc_CY']),
            c['rbc_R'],
            c['p4_X'], p.W
        )

        bottom = sum([abottom1, aline, abottom2])

        volume = top - bottom
        min_height = min_drop_nones(th1, th2, th3) - max_drop_nones(bh1, bh2,
                                                                    bh3)

        return (
            float(volume / 1000.),
            min_height
        )