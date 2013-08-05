# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#%load_ext autoreload
#%autoreload 2
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

#reload(models)
from models import *

#print model.get_volume()

#Client's precise params ----------
#
#5.0	1.5	
#5.50833333333333
#0.240997229916898
#


#5.0	1.5	
#5.50833333333333
#0.240997229916898
# l|r|t|b left right top bottom b|s big small c=circle
# C=center
# X,Y independent
# R=radius
# W=width H=height
# RI=inner ring radius

'''
But one profile we need for the testdata is.
 
P3 with 6mm width and 2,4mm height.
Ringsize only 56
 
For this profile we need the data for every 0,1mm slice.
Volume:
Profile P2:     width: 4     height:2        ringwidth/inner circumfence 56     volume:0,396 cm³
Profile P3:     width: 5     height:1,5     ringwidth/inner circumfence 56     volume:0,336 cm³
Profile P4:     width: 7     height:3        ringwidth/inner circumfence 56     volume:1,155 cm³
Profile P5:     width: 3     height:1        ringwidth/inner circumfence 56     volume:0,144 cm³
Profile P6:     width: 6     height:2,5     ringwidth/inner circumfence 56     volume:0,758 cm³
'''


profiles_definiton = load_profiles_lookup_table({})
ring_config = RingParams(W=5., H=1.5, CF=56., PROFILE='PR_003')
ring_config.lookup_definition(profiles_definiton)

ring_config.R60 = ring_config.R61 = round(5.50833333333333, 3)
ring_config.R40 = ring_config.R41 = round(0.240997229916898, 3)

print 'Using configuration:'
print ring_config

# <codecell>

context = Context()
model = globals()[ring_config.MODEL](params=ring_config, context=context)
model.create_equations()
model, context

# <codecell>


print context
print 'vars:'
print model.context.variables
print
print
print 'eq:'
print model.context.equations
print
print


# <codecell>

len(model.s_1_all), model.s_1_all, model.s_1_fil

# <codecell>

len(model.s_2_all),model.s_2_all,model.s_2_fil

# <codecell>

model.context

# <codecell>

import pandas

# <codecell>

step=0.1
slices=[]
for f in arange(0., 5., step):
    __builtin__._fr = f
    __builtin__._to = f + step
    v = model.get_volume()
    slices.append([f,f+step,v])
    

# <codecell>

a=np.array(slices);

# <codecell>

scatter(a[:,2],a[:,0])


# <codecell>

import pandas as pd
df=pd.DataFrame(a)
df.columns = ['FROM','TO','VOLUME']
df.to_excel(r'/ring/ring/volume_slices.xls')

# <codecell>


__builtin__._fr = 4.9
__builtin__._to = 5

# <codecell>

model.get_volume()

# <codecell>


