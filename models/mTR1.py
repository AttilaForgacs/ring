from models import BaseModel
from tools import *
from tools import _2_circles_tangential_equations, _2_circles_tangential_equations_constrained
from operator import itemgetter
import solver


class TR1(BaseModel):
    def __init__(self, params=None, context=None):
        super(TR1, self).__init__(params, context)

        self.context = context
        self.params = params
        c = context
        p = params

        c['lc_R'] = p.R40
        c['lc_CX'] = p.R40
        c['lc_CY'] = p.RI + p.R40

        c['rc_R'] = p.R40
        c['rc_CX'] = p.W - p.R40
        c['rc_CY'] = p.RI + p.R40


    def get_volume(self):
        c = self.context
        p = self.params
        a = p.R20 / (2 ** 0.5)

        atop1, th1 = volume_integrate_arc_top(
            P(c['lc_CX'], c['lc_CY']),
            c['lc_R'],
            0., c['lc_R']
        )

        atop2, th2 = volume_integrate_line(p.RI + p.H,
                                           c['lc_R'], p.W - c['lc_R']
        )

        atop3, th3 = volume_integrate_arc_top(
            P(c['rc_CX'], c['rc_CY']),
            c['rc_R'],
            p.W - c['rc_R'], p.W
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
            p.W-a, p.RI,
            p.W, p.RI+a,
            p.W-a, p.W
        )

        bottom = sum([abottom1, aline, abottom2])

        volume = top - bottom
        min_height = min_drop_nones(th1, th2, th3) - max_drop_nones(bh1, bh2,
                                                                    bh3)

        return (
            float(volume / 1000.),
            min_height
        )