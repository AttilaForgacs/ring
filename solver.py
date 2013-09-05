from __future__ import division


def calc_intersection(c1, c2, context):
    G = context

    c1_CX = G['{}_CX'.format(c1)]
    c1_CY = G['{}_CY'.format(c1)]
    c1_R = G['{}_R'.format(c1)]

    c2_CX = G['{}_CX'.format(c2)]
    c2_CY = G['{}_CY'.format(c2)]
    c2_R = G['{}_R'.format(c2)]

    ys = [
        ((c2_R * c1_CY + c1_R * (
            c1_CY + (
                (c1_R + c2_R + c1_CX - c2_CX) * (c1_R + c2_R - c1_CX + c2_CX))
            ** (1 / 2.)
        )) / (c1_R + c2_R)),


        ((c2_R * c1_CY + c1_R * (
            c1_CY - (
                (c1_R + c2_R + c1_CX - c2_CX) * (
                    c1_R + c2_R - c1_CX + c2_CX)) ** (
                1 / 2. ))) / (c1_R + c2_R)),


        (-(c2_R * c1_CY - c1_R * (
            c1_CY + (
                (c1_R - c2_R + c1_CX - c2_CX) * (
                    c1_R - c2_R - c1_CX + c2_CX)) ** (
                1 / 2.))) / (c1_R - c2_R)),


        (-(c2_R * c1_CY - c1_R * (
            c1_CY - (
                (c1_R - c2_R + c1_CX - c2_CX) * (
                    c1_R - c2_R - c1_CX + c2_CX)) ** (
                1 / 2.))) / (c1_R - c2_R))
    ]

    xs = [
        ((c1_R * c2_CX + c2_R * c1_CX) / float(c1_R + c2_R)),
        ((c1_R * c2_CX + c2_R * c1_CX) / float(c1_R + c2_R)),
        ((c1_R * c2_CX - c2_R * c1_CX) / float(c1_R - c2_R)),
        ((c1_R * c2_CX - c2_R * c1_CX) / float(c1_R - c2_R)),
    ]

    c2ys = [

        (c1_CY + (
            (c1_R + c2_R + c1_CX - c2_CX) * (c1_R + c2_R - c1_CX + c2_CX)) ** (
             1 / 2.)),

        (c1_CY - (
            (c1_R + c2_R + c1_CX - c2_CX) * (c1_R + c2_R - c1_CX + c2_CX)) ** (
             1 / 2.)),

        (c1_CY + (
            (c1_R - c2_R + c1_CX - c2_CX) * (c1_R - c2_R - c1_CX + c2_CX)) ** (
             1 / 2.)),

        (c1_CY - (
            (c1_R - c2_R + c1_CX - c2_CX) * (c1_R - c2_R - c1_CX + c2_CX)) ** (
             1 / 2.)),

    ]

    res = xs, ys, c2ys
    return zip(res[0], res[1], res[2])


def calc_line_vs_circle_intersections(c1, x1, y1, x2, y2, context):
    G = context

    p1_X = x1
    p1_Y = y1
    p2_X = x2
    p2_Y = y2

    c_CX = G['{}_CX'.format(c1)]
    c_CY = G['{}_CY'.format(c1)]
    c_R = G['{}_R'.format(c1)]

    xs = [
        (p1_X * p2_X - p1_X * p2_Y + (p1_X * (p2_Y * (
                                                         2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p1_X ** 2 - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                                                         1 / 2) - p1_X * (
                                                                             2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p1_X ** 2 - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                                                                             1 / 2) + c_CX * p1_X ** 2 + c_CY * p1_X ** 2 + c_CY * p2_Y ** 2 + p1_X * p2_X ** 2 - p1_X ** 2 * p2_X + p1_X ** 2 * p2_Y - c_CX * p1_X * p2_X - c_CX * p1_X * p2_Y + c_CX * p2_X * p2_Y - 2 * c_CY * p1_X * p2_Y - p1_X * p2_X * p2_Y)) / (
             2 * p1_X ** 2 - 2 * p1_X * p2_X - 2 * p1_X * p2_Y + p2_X ** 2 + p2_Y ** 2) - (
             p2_X * (p2_Y * (
                                2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p1_X ** 2 - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                                1 / 2) - p1_X * (
                                                    2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p1_X ** 2 - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                                                    1 / 2) + c_CX * p1_X ** 2 + c_CY * p1_X ** 2 + c_CY * p2_Y ** 2 + p1_X * p2_X ** 2 - p1_X ** 2 * p2_X + p1_X ** 2 * p2_Y - c_CX * p1_X * p2_X - c_CX * p1_X * p2_Y + c_CX * p2_X * p2_Y - 2 * c_CY * p1_X * p2_Y - p1_X * p2_X * p2_Y)) / (
             2 * p1_X ** 2 - 2 * p1_X * p2_X - 2 * p1_X * p2_Y + p2_X ** 2 + p2_Y ** 2)) / (
            p1_X - p2_Y)
        ,
        (p1_X * p2_X - p1_X * p2_Y + (p1_X * (p1_X * (
                                                         2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p1_X ** 2 - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                                                         1 / 2) - p2_Y * (
                                                                             2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p1_X ** 2 - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                                                                             1 / 2) + c_CX * p1_X ** 2 + c_CY * p1_X ** 2 + c_CY * p2_Y ** 2 + p1_X * p2_X ** 2 - p1_X ** 2 * p2_X + p1_X ** 2 * p2_Y - c_CX * p1_X * p2_X - c_CX * p1_X * p2_Y + c_CX * p2_X * p2_Y - 2 * c_CY * p1_X * p2_Y - p1_X * p2_X * p2_Y)) / (
             2 * p1_X ** 2 - 2 * p1_X * p2_X - 2 * p1_X * p2_Y + p2_X ** 2 + p2_Y ** 2) - (
             p2_X * (p1_X * (
                                2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p1_X ** 2 - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                                1 / 2) - p2_Y * (
                                                    2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p1_X ** 2 - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                                                    1 / 2) + c_CX * p1_X ** 2 + c_CY * p1_X ** 2 + c_CY * p2_Y ** 2 + p1_X * p2_X ** 2 - p1_X ** 2 * p2_X + p1_X ** 2 * p2_Y - c_CX * p1_X * p2_X - c_CX * p1_X * p2_Y + c_CX * p2_X * p2_Y - 2 * c_CY * p1_X * p2_Y - p1_X * p2_X * p2_Y)) / (
             2 * p1_X ** 2 - 2 * p1_X * p2_X - 2 * p1_X * p2_Y + p2_X ** 2 + p2_Y ** 2)) / (
            p1_X - p2_Y)
    ]

    ys = [

        (p2_Y * (
                    - c_CX ** 2 * p1_X ** 2 + 2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                    1 / 2) - p1_X * (
                                        - c_CX ** 2 * p1_X ** 2 + 2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                                        1 / 2) + c_CX * p1_X ** 2 + c_CY * p1_X ** 2 + c_CY * p2_Y ** 2 + p1_X * p2_X ** 2 - p1_X ** 2 * p2_X + p1_X ** 2 * p2_Y - c_CX * p1_X * p2_X - c_CX * p1_X * p2_Y + c_CX * p2_X * p2_Y - 2 * c_CY * p1_X * p2_Y - p1_X * p2_X * p2_Y) / (
            2 * p1_X ** 2 - 2 * p1_X * p2_X - 2 * p1_X * p2_Y + p2_X ** 2 + p2_Y ** 2),

        (p1_X * (
                    - c_CX ** 2 * p1_X ** 2 + 2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                    1 / 2) - p2_Y * (
                                        - c_CX ** 2 * p1_X ** 2 + 2 * c_CX ** 2 * p1_X * p2_Y - c_CX ** 2 * p2_Y ** 2 + 2 * c_CX * c_CY * p1_X ** 2 - 2 * c_CX * c_CY * p1_X * p2_X - 2 * c_CX * c_CY * p1_X * p2_Y + 2 * c_CX * c_CY * p2_X * p2_Y + 2 * c_CX * p1_X ** 2 * p2_X - 2 * c_CX * p1_X ** 2 * p2_Y - 2 * c_CX * p1_X * p2_X * p2_Y + 2 * c_CX * p1_X * p2_Y ** 2 - c_CY ** 2 * p1_X ** 2 + 2 * c_CY ** 2 * p1_X * p2_X - c_CY ** 2 * p2_X ** 2 - 2 * c_CY * p1_X ** 2 * p2_X + 2 * c_CY * p1_X ** 2 * p2_Y + 2 * c_CY * p1_X * p2_X ** 2 - 2 * c_CY * p1_X * p2_X * p2_Y + 2 * c_R ** 2 * p1_X ** 2 - 2 * c_R ** 2 * p1_X * p2_X - 2 * c_R ** 2 * p1_X * p2_Y + c_R ** 2 * p2_X ** 2 + c_R ** 2 * p2_Y ** 2 - p1_X ** 2 * p2_X ** 2 + 2 * p1_X ** 2 * p2_X * p2_Y - p1_X ** 2 * p2_Y ** 2) ** (
                                        1 / 2) + c_CX * p1_X ** 2 + c_CY * p1_X ** 2 + c_CY * p2_Y ** 2 + p1_X * p2_X ** 2 - p1_X ** 2 * p2_X + p1_X ** 2 * p2_Y - c_CX * p1_X * p2_X - c_CX * p1_X * p2_Y + c_CX * p2_X * p2_Y - 2 * c_CY * p1_X * p2_Y - p1_X * p2_X * p2_Y) / (
            2 * p1_X ** 2 - 2 * p1_X * p2_X - 2 * p1_X * p2_Y + p2_X ** 2 + p2_Y ** 2)
    ]

    res = xs, ys
    return zip(res[0], res[1])


def circle_subst(c1, x, context):
    G = context
    X = x
    c_CX = float(G['{}_CX'.format(c1)])
    c_CY = float(G['{}_CY'.format(c1)])
    c_R = float(G['{}_R'.format(c1)])

    ys = [
        (c_CY + (X - c_CX + c_R) ** (1 / 2) * (c_CX - X + c_R) ** (1 / 2)),
        (c_CY - (X - c_CX + c_R) ** (1 / 2) * (c_CX - X + c_R) ** (1 / 2))
    ]

    return ys

# if __name__ == '__main__':
#     c = dict()
#     c['lc_R'] = 1
#     c['lc_CX'] = 2
#     c['lc_CY'] = 3
#     c['rc_R'] = 4
#     c['rc_CX'] = 5
#     c['rc_CY'] = 6
#
#     res = calc_intersection(
#         'lc', 'rc', c
#     )
#
#     print res
#     print zip(res[0], res[1], res[2])


# if __name__ == '__main__':
#     c = dict()
#     c['lc_R'] = 10
#     c['lc_CX'] = 0
#     c['lc_CY'] = 0
#
#     print calc_line_vs_circle_intersections('lc', -5, -5, 10, 10, c)


# if __name__ == '__main__':
#     c = dict()
#     c['lc_R'] = 10
#     c['lc_CX'] = 0
#     c['lc_CY'] = 0
#     print circle_subst('lc', -10, c)

