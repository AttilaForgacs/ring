

from __future__ import division
import __builtin__
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
from sympy import init_printing;init_printing()
from models import *

# <codecell>

profiles_definiton = load_profiles_lookup_table({})
ring_config = RingParams(W=5., H=1.5, CF=56., PROFILE='PR_001')
ring_config.lookup_definition(profiles_definiton)

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

def a():
    prec=2
    for i in xrange(62, len(widths)):
        w=widths[i].value
        h=heights[i].value
        r60=r60s[i].value
        r61=r61s[i].value
        r40=r40s[i].value
        r41=r41s[i].value
        if r40 and r41 and r61:
            ring_config = RingParams(W=5., H=1.5, CF=56., PROFILE='PR_001')
            ring_config.lookup_definition(profiles_definiton)
            ring_config.W = round(w,prec)
            ring_config.H = round(h,prec)
            ring_config.R60 = round(r60,prec)
            ring_config.R61 = round(r61,prec)
            ring_config.R40 = round(r40,prec)
            ring_config.R41 = round(r41,prec)        
            print '%s Using configuration:'%(i)
            print ring_config
            context = Context()
            model = globals()[ring_config.MODEL](params=ring_config, context=context)
            model.create_equations()        
            print 'Vol:',model.get_volume()

# <codecell>

# <codecell>

slices=[]
prec=2
i = 2
w=widths[i].value
h=heights[i].value
r60=r60s[i].value
r61=r61s[i].value
r40=r40s[i].value
r41=r41s[i].value
print time.time()
if r40 and r41 and r61:
    ring_config = RingParams(W=5., H=1.5, CF=56., PROFILE='PR_001')
    ring_config.lookup_definition(profiles_definiton)
    ring_config.W = round(w,prec)
    ring_config.H = round(h,prec)
    ring_config.R60 = round(r60,prec)
    ring_config.R61 = round(r61,prec)
    ring_config.R40 = round(r40,prec)
    ring_config.R41 = round(r41,prec)        
    print '%s Using configuration:'%(i)
    print ring_config
    context = Context()
    model = globals()[ring_config.MODEL](params=ring_config, context=context)
    model.create_equations()        
    #print 'Vol:',model.get_volume()
    print time.time()
    print '...>'
    step=0.1    
    for f in arange(0., 5., step):
        __builtin__._fr = f
        __builtin__._to = f + step
        v,h = model.get_volume()
        slices.append([f,f+step,v,h])
        print [f,f+step,v,h]
        print time.time()
        
        
print slices

# <codecell>

plot([x[3] for x in slices])

# <codecell>

[ abs(round(float(x[3]),2)) for x in slices ]

# <codecell>

plot([ abs(round(float(x[2]),10)) for x in slices ],'r--')

