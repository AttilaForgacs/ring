# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from sympy import *
import numpy as np
import scipy as sp
%load_ext sympyprinting
#%load_ext sympy.interactive.ipythonprintingthonprinting
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

W  = 6. #R51 
H  = 1.8 #R52
RI = 7.4  
bbc_R  = 6.38
btc_R  = 6.38
# calculated
bbc_CX = W/2.
bbc_CY = RI + bbc_R
btc_CX = W/2.
btc_CY = RI + H - btc_R
lsc_R  = Symbol('lsc_R',positive=True)
lsc_CX = Symbol('lsc_CX')
lsc_CY = Symbol('lsc_CY')
rsc_R  = Symbol('rsc_R',positive=True)
rsc_CX = Symbol('rsc_CX')
rsc_CY = Symbol('rsc_CY')

# <codecell>

# left and right centerX's of small circles
eq_left_tang = lsc_CX - lsc_R 
eq_right_tang = rsc_CX - W + rsc_R  
# 4 tangent. of small circles crossing big circles
# e.g. ('lsc','bsc','p1')
def _2_circles_tangential_equations(c1,c2,var_name,variables_list):
    'c1: string name of circle 1'
    'c2: string name of other circle'
    'var_name: string, independent will be created'
    G = globals()
    c1_CX = G['{}_CX'.format(c1)]
    c1_CY = G['{}_CY'.format(c1)]
    c1_R  = G['{}_R'.format(c1)]

    c2_CX = G['{}_CX'.format(c2)]
    c2_CY = G['{}_CY'.format(c2)]
    c2_R  = G['{}_R'.format(c2)]
    X = Symbol(var_name+'_X')
    Y = Symbol(var_name+'_Y')
    variables_list += [X,Y]
    eq_c1 = (X - c1_CX) ** 2 + (Y - c1_CY) ** 2 - c1_R ** 2
    eq_c2 = (X - c2_CX) ** 2 + (Y - c2_CY) ** 2 - c2_R ** 2
    eq_line = (Y - c2_CY) * (c1_CX - c2_CX) - (X - c2_CX) * (c1_CY - c2_CY)
    return [eq_c1, eq_c2, eq_line]

# <codecell>

eq_system = []
variables = []

eq_system += _2_circles_tangential_equations('lsc','btc','p1',variables)
eq_system += _2_circles_tangential_equations('lsc','bbc','p3',variables)
eq_system += _2_circles_tangential_equations('rsc','btc','p2',variables)
eq_system += _2_circles_tangential_equations('rsc','bbc','p4',variables)
eq_system += [eq_left_tang]
eq_system += [eq_right_tang]
variables += [lsc_CX,lsc_CY,lsc_R]
variables += [rsc_CX,rsc_CY,rsc_R]

eq_system[::-1] 

# <codecell>

variables

# <codecell>

#from sympy import ask, Q
#global_assumptions.add(Q.positive(lsc_R))

solutions = solve(   eq_system , *variables , dict=True )

# <codecell>

len(solutions) ,  solutions

# <codecell>

filtered_solutions = [ s 
for s in solutions
if RI+H >s[lsc_CY]> RI and
   RI+H >s[rsc_CY]> RI
]
len(filtered_solutions)

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
#fig = plt.figure(figsize=(10,10*(H/W)))
fig = plt.figure(figsize=(10,10))
rr=1000
margin=20
plt.xlim([0-margin,W+margin])
plt.ylim([RI-margin,RI+H+margin])
ax = fig.add_subplot(1, 1, 1)

def mk_circle(x,y,r,**kwargs):
    circ = plt.Circle((x, y),r, fill=False, **kwargs)
    plt.gcf().gca().add_artist(circ)
    return circ
    
mk_circle(bbc_CX,bbc_CY,bbc_R)
mk_circle(btc_CX,btc_CY,btc_R)

for s in filtered_solutions:
    mk_circle( s[lsc_CX],s[lsc_CY],s[lsc_R],color='r')
    mk_circle( s[rsc_CX],s[rsc_CY],s[rsc_R],color='g')
    
#line1 = plt.Line2D([plot_x,bbc_CX],[plot_y,plot_cy])
#plt.gcf().gca().add_artist(line1)

assert len (filtered_solutions) == 1
S = filtered_solutions[0]

plt.show()

# <codecell>

%run integral.py

# <codecell>

P(S[lsc_CX],S[lsc_CY])

# <codecell>

volume = __builtin__.sum (
   [integrate_arc_top(P(S[lsc_CX],S[lsc_CY]), S[lsc_R], 0., S[Symbol('p1_X')]),
   integrate_arc_top(P(btc_CX,btc_CY), btc_R, S[Symbol('p1_X')], S[Symbol('p2_X')])]
) - 0

#btc_CX,btc_CY
#S[Symbol('p1_X')], S[Symbol('p2_X')], btc_CX,btc_R,

volume

# <codecell>

#%run integral.py
integrate_arc_top(P(btc_CX,btc_CY), btc_R, S[Symbol('p1_X')], S[Symbol('p2_X')])

# <codecell>

(0.211 - 3)**2
S[Symbol('p1_X')],S[Symbol('p2_X')]

# <codecell>

rng=arange(S[Symbol('p1_X')], S[Symbol('p2_X')] ,0.01)
plt.figure(111)
plt.figsize(5,5)
plot(map(lambda x:f_top_arc(x,P(btc_CX,btc_CY),btc_R),rng))

# <codecell>


