import tools
import models
import xlrd
import collections
import pprint
import itertools
import numpy as np
import csv
import __builtin__

def pr_to_tr(pr):
    '''
    returns like: TR4
    '''
    ctx = tools.load_profiles_lookup_table({})
    return ctx[pr]['TR_CODE']


def process_pr(pr):
    excelfile = './parameters/%s_Daten.xlsx' % pr
    assert open(excelfile)
    csvfile = open('/home/attila/ringdong/%s.csv' % pr, 'wb+')

    ringwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    tr_code = pr_to_tr(pr)
    assert len(tr_code) > 2
    model_ref = models.__dict__[tr_code]
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

    #TODO header
    # ringwriter.writerow(
    #     list(parameters.keys()) + list(
    #         itertools.chain(*zip(_volumes, _heights))))

    for CF in xrange(460, 760, 5):
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

            #print 'Vol:', model.get_volume()

            step = 0.1
            _volumes = []
            _heights = []

            for f in np.arange(0., w, step):
                __builtin__._fr = f
                __builtin__._to = f + step
                vol, hei = model.get_volume()
                _volumes.append(float(vol))
                _heights.append(float(hei))

            _heights[-1] = 0 # trim the sunci

            ringwriter.writerow(
                list(map(lambda k: parameters[k][i], parameters.keys())) +
                list(itertools.chain(*zip(_volumes, _heights)))
            )
            csvfile.flush()

    csvfile.close()


if __name__ == '__main__':
    process_pr('PR_006')

