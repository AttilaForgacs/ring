# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%pylab inline

# <codecell>

%load_ext autoreload
%autoreload 1

# <codecell>

from __future__ import division
from pylab import *
from tools import *
import itertools
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
%aimport models
%aimport tools
from sympy import init_printing;init_printing()
from models import *

# <codecell>

%aimport models

# <codecell>

models.TR13.__module__

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

len(widths)

# <codecell>

%%time
try:
    del __builtin__._fr 
    del __builtin__._to 
except:
    pass


import csv
csvfile=open('/home/attila/Desktop/PR_001.csv', 'wb+') 
ringwriter = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)

import gc

#CF 46-76, step : 0.5

def calc_full_profile():
    prec=23
    for CF in xrange(460,760,5):
        for i in xrange(1, len(widths)):
            
            w=widths[i].value
            h=heights[i].value
            r60=r60s[i].value
            r61=r61s[i].value
            r40=r40s[i].value
            r41=r41s[i].value
            r20=''
            p1=''
            p2=''
    
            if r40 and r41 and r61:
                ring_config = RingParams(W=round(w,prec), H=round(h,prec), CF=CF / 10., PROFILE='PR_001')
                ring_config.lookup_definition(profiles_definiton)
                ring_config.R60 = round(r60,prec)
                ring_config.R61 = round(r61,prec)
                ring_config.R40 = round(r40,prec)
                ring_config.R41 = round(r41,prec)        
                print '%s Using configuration CF %s'%(i,CF)
                print ring_config
                context = Context()
                model = globals()[ring_config.MODEL](params=ring_config, context=context)
                model.create_equations()        
                #print 'Vol:',model.get_volume()
                #plt.savefig('/home/attila/Desktop/RING_%s.png'%i)     
                #plt.clf()
                #plt.close()
                
                
                
                
                step=0.1    
                _volumes=[]
                _heights=[]
                
                for f in arange(0., w, step):
                    __builtin__._fr = f
                    __builtin__._to = f + step                
                    vol,hei = model.get_volume()
                    _volumes.append(float(vol))
                    _heights.append(float(hei))            
                
                _heights[-1] = 0
                
                ringwriter.writerow([CF/10.,w,h,r60,r61,r40,r41,r20,p1,p2]+list( itertools.chain( *zip(_volumes,_heights) )   ) )                               
                csvfile.flush()
                gc.collect()
                
                

# <codecell>

%%time
calc_full_profile()

# <codecell>


# <codecell>

%%time
slices=[]
prec=3
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
    try:
        del __builtin__._fr 
        del __builtin__._to 
    except:
        pass

    print 'Vol:',model.get_volume()
    
    print '...>'
    step=0.1    
    for f in arange(0., 5., step):
        __builtin__._fr = f
        __builtin__._to = f + step
        v,h = model.get_volume()
        slicesa().append([f,f+step,v,h])
        print [f,f+step,v,h]
                    
print slices

# <codecell>

plot([x[3] for x in slices])

# <codecell>

[ round(float(x[3]),5) for x in slices ]

# <codecell>

23plot([ abs(round(float(x[2]),10)) for x in slices ],'r--')

