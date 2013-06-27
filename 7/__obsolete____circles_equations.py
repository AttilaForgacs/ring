# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from sympy import *
import numpy as np
import scipy as sp
%load_ext sympyprinting
#%load_ext sympy.interactive.ipythonprinting
#%pylab inline
from __future__ import division
init_printing()
# l|r|t|b left right top bottom b|s big small c=circle
# C=center 
# X,Y independent
# R=radius
# W=width H=height
# RI=inner ring radius

# <codecell>

W = 277. 
H = 100.
RI=740.; 
lsc_CX,lsc_CY = 23.  , RI+40.
lsc_R = 23.
bbc_CX = W/2.
bbc_R = 357.

# <codecell>

bbc_CY,X,Y=symbols('bbc_CY X Y')

# <codecell>

eq_lsc = (X-lsc_CX)**2+(Y-lsc_CY)**2 - lsc_R**2
eq_bbc = (X-bbc_CX)**2+(Y-bbc_CY)**2 - bbc_R**2
eq_line = (Y-bbc_CY)*(lsc_CX-bbc_CX) - (X-bbc_CX)*(lsc_CY-bbc_CY)

# <codecell>

solutions = solve(   [eq_lsc,eq_bbc,eq_line] , bbc_CY, X, Y)
print "solutions:", len(solutions)
assert len(solutions) == 4

# <codecell>

print "solutions"
for s in solutions:
    print s
from operator import itemgetter
plot_cy,plot_x,plot_y=sorted(solutions, key=itemgetter(0), reverse=1)[1]

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
#_x, _y = np.meshgrid(np.linspace(0,1), np.linspace(0,1))
#F = _x ** _y
#G = _y ** _x
fig = plt.figure(figsize=(10,10*(H/W)))
rr=1000
margin=20
plt.xlim([0-margin,W+margin])
plt.ylim([RI-margin,RI+H+margin])
ax = fig.add_subplot(1, 1, 1)
circ = plt.Circle((bbc_CX, plot_cy),bbc_R, color='r', fill=False)
plt.gcf().gca().add_artist(circ)

circ2 = plt.Circle((lsc_CX, lsc_CY),lsc_R, color='blue', fill=False)
plt.gcf().gca().add_artist(circ2)

line1 = plt.Line2D([plot_x,bbc_CX],[plot_y,plot_cy])
plt.gcf().gca().add_artist(line1)

plt.show()

