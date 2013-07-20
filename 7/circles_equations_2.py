# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from sympy import *
import numpy as np
import scipy as sp
import time
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

'''
Volume:
Profile P2:     width: 4     height:2        ringwidth/inner circumfence 56     volume:0,396 cm³
Profile P3:     width: 5     height:1,5     ringwidth/inner circumfence 56     volume:0,336 cm³
Profile P4:     width: 7     height:3        ringwidth/inner circumfence 56     volume:1,155 cm³
Profile P5:     width: 3     height:1        ringwidth/inner circumfence 56     volume:0,144 cm³
Profile P6:     width: 6     height:2,5     ringwidth/inner circumfence 56     volume:0,758 cm³
'''

#R51, R52
W=3.
H=1.
CF = 56
RI = (CF / (2.*pi) )
RI = round(RI,6)

#R60
bbc_R  = 5.2
#R61
btc_R  = 25.6

# <codecell>

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

#
#
#
W,H,RI
bbc_CX,bbc_CY,btc_CX,btc_CY
RI+1.5/2
print 'RI=%s RI+1.5=%s',RI, RI+1.5

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
(eq_left_tang, eq_right_tang)

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

t1=time.time()
solutions = solve(   eq_system , *variables , dict=True )
t2=time.time()
print 'Solution: %s seconds'%(t2-t1)

# <codecell>

len(solutions) ,  solutions

# <codecell>

filtered_solutions = [ s 
for s in solutions
if RI+H >s[lsc_CY]> RI and
   RI+H >s[rsc_CY]> RI
]
len(filtered_solutions)
for s in filtered_solutions[0]:
    print s,'\t:',filtered_solutions[0][s]

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

plt.figsize(20,10)
plt.gca().set_xlim(-1,W+1)
plt.gca().set_ylim(RI-1,H+RI+1)

top = __builtin__.sum ([
   volume_integrate_arc_top(P(S[lsc_CX],S[lsc_CY]), S[lsc_R], 0., S[Symbol('p1_X')]),
   volume_integrate_arc_top(P(btc_CX,btc_CY), btc_R, S[Symbol('p1_X')], S[Symbol('p2_X')]),
   volume_integrate_arc_top(P(S[rsc_CX],S[rsc_CY]), S[rsc_R], S[Symbol('p2_X')], W),
]) 
bottom = __builtin__.sum ([
   volume_integrate_arc_bottom(P(S[lsc_CX],S[lsc_CY]), S[lsc_R], 0. , S[Symbol('p3_X')]),
   volume_integrate_arc_bottom(P(bbc_CX,bbc_CY), bbc_R, S[Symbol('p3_X')], S[Symbol('p4_X')]),
   volume_integrate_arc_bottom(P(S[rsc_CX],S[rsc_CY]), S[rsc_R], S[Symbol('p4_X')], W),             
]) 

print 'top_vol=',top
print 'bottom_vol=',bottom
volume=top-bottom
print 'vol=',volume

# <codecell>

[
   volume_integrate_arc_top(P(S[lsc_CX],S[lsc_CY]), S[lsc_R], 0., S[Symbol('p1_X')]),
   volume_integrate_arc_top(P(btc_CX,btc_CY), btc_R, S[Symbol('p1_X')], S[Symbol('p2_X')]),
   volume_integrate_arc_top(P(S[rsc_CX],S[rsc_CY]), S[rsc_R], S[Symbol('p2_X')], W),
]

# <codecell>

[
   volume_integrate_arc_bottom(P(S[lsc_CX],S[lsc_CY]), S[lsc_R], 0. , S[Symbol('p3_X')]),
   volume_integrate_arc_bottom(P(bbc_CX,bbc_CY), bbc_R, S[Symbol('p3_X')], S[Symbol('p4_X')]),
   volume_integrate_arc_bottom(P(S[rsc_CX],S[rsc_CY]), S[rsc_R], S[Symbol('p4_X')], W),             
]

# <codecell>

volume_integrate_arc_top(P(S[lsc_CX],S[lsc_CY]), S[lsc_R], 0., S[Symbol('p1_X')])

# <codecell>

volume_integrate_arc_top(P(btc_CX,btc_CY), btc_R, S[Symbol('p1_X')], S[Symbol('p2_X')])

# <codecell>

volume_integrate_arc_top(P(S[rsc_CX],S[rsc_CY]), S[rsc_R], S[Symbol('p2_X')], W)

# <rawcell>

# So far I have  only send you the final data for profiles p2-p6.
# (but maybe you are reffering to the structure PDF TR_7.pdf)
#  
# For those profiles I have sent you the volume-values to quick validate the calculations
#  
# Volume:
# Profile P2:     width: 4     height:2        ringwidth/inner circumfence 56     volume:0,396 cm³
# Profile P3:     width: 5     height:1,5     ringwidth/inner circumfence 56     volume:0,336 cm³
# Profile P4:     width: 7     height:3        ringwidth/inner circumfence 56     volume:1,155 cm³
# Profile P5:     width: 3     height:1        ringwidth/inner circumfence 56     volume:0,144 cm³
# Profile P6:     width: 6     height:2,5     ringwidth/inner circumfence 56     volume:0,758 cm³

# <codecell>

ours = 155.559839915
theirs = 144
diff = ours - theirs
deviation = diff / min(theirs,ours)
print 'difference=',diff
print 'dev =',deviation*100,' %'

