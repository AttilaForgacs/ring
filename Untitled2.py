# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import xlrd

# <codecell>

import xlrd
book = xlrd.open_workbook('./parameters/PR_001_Daten.xlsx')

# <codecell>

s=book.sheet_by_index(0)

# <codecell>

s.col(2)

# <codecell>


