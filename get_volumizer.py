# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%pylab inline

# <codecell>

from __future__ import division
from pylab import *
from tools import *
from collections import *
from math import *
from numpy import array, cos, sin
import functools
import scipy
import sympy
from IPython.display import Image
from scipy.integrate import quad
from sympy import *
import numpy as np
import scipy as sp
import time
import models
from sympy import init_printing;init_printing()
from models import *

# <codecell>

profiles_definiton = load_profiles_lookup_table({})
ring_config = RingParams(W=5., H=1.5, CF=56., PROFILE='PR_001')
ring_config.lookup_definition(profiles_definiton)

# override ########
ring_config.W = 2.5
ring_config.H = 1.
ring_config.R60 = 0.
ring_config.R61 = round(2.17718474478179, 3)
ring_config.R40 = round(0.35,3)
ring_config.R41 = round(0.455863932713471,3)

print 'Using configuration:'
print ring_config
context = Context()
model = globals()[ring_config.MODEL](params=ring_config, context=context)
model.create_equations()

# <codecell>

solutions = model.solve()
print solutions
volume = model.get_volume()

# <codecell>

volume

# <codecell>

import xlrd
book = xlrd.open_workbook('./parameters/PR_001_Daten.xlsx')

# <codecell>

s=book.sheet_by_index(0)

# <codecell>

widths=s.col(2)
heights=s.col(3)
r60s=s.col(4)
r61s=s.col(5)
r40s=s.col(6)
r41s=s.col(7)

# <codecell>

for i in xrange(1,len(widths)):
    w=widths[i].value
    h=heights[i].value
    r60=r60s[i].value
    r61=r61s[i].value
    r40=r40s[i].value
    r41=r41s[i].value
    if r40 and r41 and r61:
        ring_config = RingParams(W=5., H=1.5, CF=56., PROFILE='PR_001')
        ring_config.lookup_definition(profiles_definiton)
        ring_config.W = w
        ring_config.H = h
        ring_config.R60 = round(r60,3)
        ring_config.R61 = round(r61,3)
        ring_config.R40 = round(r40,3)
        ring_config.R41 = round(r41,3)        
        print 'Using configuration:'
        print ring_config
        context = Context()
        model = globals()[ring_config.MODEL](params=ring_config, context=context)
        model.create_equations()        
        print 'Vol:',model.get_volume()

