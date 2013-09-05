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


if __name__ == '__main__':
    c = dict()
    c['lc_R'] = 1
    c['lc_CX'] = 2
    c['lc_CY'] = 3
    c['rc_R'] = 4
    c['rc_CX'] = 5
    c['rc_CY'] = 6

    res = calc_intersection(
        'lc', 'rc', c
    )

    print res
    print zip(res[0], res[1], res[2])