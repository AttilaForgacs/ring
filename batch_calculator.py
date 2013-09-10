import tools
import models
import xlrd
import pprint


def pr_to_tr(pr):
    '''
    returns like: TR4
    '''
    ctx = tools.load_profiles_lookup_table({})
    return ctx[pr]['TR_CODE']


def process_pr(pr):
    excelfile = './parameters/%s_Daten.xlsx' % pr
    assert open(excelfile)
    tr_code = pr_to_tr(pr)
    assert len(tr_code) > 2
    model_ref = models.__dict__[tr_code]
    book = xlrd.open_workbook(excelfile)
    sheet = book.sheet_by_index(0)

    parameters = {}
    for i in range(2, sheet.ncols):
        col = sheet.col(i)
        id = str(col[0].value)
        parameters[id] = []
        for idx, row in enumerate(col):
            if idx == 0: continue
            parameters[id].append(row.value)

    parameter = None

    for CF in xrange(460, 760, 5):
        for i in range(0, sheet.nrows):

            parameter = tools.RingParams(
                W=parameters['R51'][i],
                H=parameters['R52'][i],
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
            print 'Vol:', model.get_volume()


if __name__ == '__main__':
    process_pr('PR_006')

