import resource
import sys
import tools
import models
import xlrd
import collections
import pprint
import itertools
import numpy as np
import csv
import __builtin__
from itertools import chain
import argparse
import time

ctx = tools.load_profiles_lookup_table({})

USE_SINGLE_FILE_PARAMETER = True


def pr_to_tr(pr):
    '''
    returns like: TR4
    '''
    global ctx
    return ctx[pr]['TR_CODE']


def zerobased_index(n):
    n = n[3:]
    return int(n, 10) - 1


def process_pr(pr):
    out_csv_file = open('/media/attila/terra/ring_csv/%s.csv' % pr, 'wb+')

    ringwriter = csv.writer(out_csv_file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # TR lookup
    tr_code = pr_to_tr(pr)
    assert len(tr_code) > 2
    model_ref = models.__dict__[tr_code]

    # Input excel: collection 1-24.xlsx
    if USE_SINGLE_FILE_PARAMETER:
        excelfile = './parameters/PR_001-PR_024.xlsx'
        assert open(excelfile)
        book = xlrd.open_workbook(excelfile)
        sheet = book.sheet_by_index(zerobased_index(pr))
    # Input excel: many files...
    else:
        excelfile = './parameters/%s_Daten.xlsx' % pr
        assert open(excelfile)
        book = xlrd.open_workbook(excelfile)
        sheet = book.sheet_by_index(0)

    parameters = collections.OrderedDict()

    for i in range(2, sheet.ncols):
        col = sheet.col(i)
        id = str(col[0].value)
        parameters[id] = []
        for idx, row in enumerate(col):
            if idx == 0: continue
            parameters[id].append(row.value)

    parameter = None
    w, h = 0, 0
    max_width = max(parameters['R51'])

    ringwriter.writerow(
        ['CF'] +
        list(parameters.keys()) +
        list(chain.from_iterable(
            map(lambda x: ['v%s' % (x), 'h%s' % (x)],
                range(0, int(max_width * 10)))
        ))
    )

    all_cirumferences = xrange(460, 760, 5)

    for CF in all_cirumferences:
        for i in range(0, sheet.nrows - 1):

            w = parameters['R51'][i]
            h = parameters['R52'][i]

            parameter = tools.RingParams(
                W=w,
                H=h,
                CF=CF / 10.,
                PROFILE=pr,
            )

            non_empty_params = 0

            for key in parameters.keys():
                param_value = parameters[key][i]
                setattr(parameter, key, param_value)
                if param_value != '':
                    non_empty_params += 1

            if non_empty_params == 2:
                # not enough data, skip
                continue

            model = model_ref(params=parameter, context=tools.Context())
            model.calculate_intersections()

            #print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.


            step = 0.1
            _volumes = []
            _heights = []

            for f in np.arange(0., w, step):
                __builtin__._fr = f
                __builtin__._to = f + step
                vol, hei = model.get_volume()
                if vol < 0.0000000000001: vol = 0.
                if hei < 0.0000000000001: hei = 0.
                _volumes.append(float(vol))
                _heights.append(float(hei))

            _heights[-1] = 0

            ringwriter.writerow(
                [CF / 10.] +
                list(map(lambda k: parameters[k][i], parameters.keys())) +
                list(itertools.chain(*zip(_volumes, _heights)))
            )
            out_csv_file.flush()

    out_csv_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Ring Slicer 0.3b'
    )

    parser.add_argument(action="store", dest="profile_name", type=str,
                        help="e.g. PR_006"
    )

    arguments = parser.parse_args()

    process_pr(arguments.profile_name)

