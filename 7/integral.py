# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from pylab import *

from collections import *

from math import *
from numpy import array, cos, sin

import functools
import scipy
import sympy
P = namedtuple('Point', ['x', 'y']);
def area_rectangle_tl_br(tl,br):
    return abs(tl.x-br.x) * abs(tl.y-br.y)
from IPython.display import Image
from scipy.integrate import quad
#degrees = 180 * radians / pi
#radians = pi * degrees / 180
#%pylab
#%load_ext sympy.interactive.ipythonprinting
from decimal import *
def assert_floats_equal(a,b):
    return Decimal(a) == Decimal(b)

# <codecell>

def vector_length(pa,pb):
    return sqrt( (pa.x - pb.x)**2 + (pa.y - pb.y)**2 )
def get_angle_between_3_points(pc, p1, p2):
    """ pc=point center, p1,p2 """
    vl = vector_length
    return arccos ( ( vl(pc,p1)**2 + vl(pc,p2)**2 - vl(p1,p2)**2 ) / (2*vl(pc,p1)*vl(pc,p2)) )
#get_angle_between_3_points( P(0,0), P(0,1), P(1,0)  )    

# <codecell>

def area_pie_slice(pc,p1,p2): 
    "get area of circle-slice center(pc), 2 points on cirlce (p1,p2)"
    r = vector_length(pc,p1)
    area_cirlce = (r*r)*pi
    return area_cirlce * (get_angle_between_3_points(pc,p1,p2) / (2.*pi))  
assert abs(   area_pie_slice ( P(0,0), P(0,1), P(1,0)  ) - pi/4   ) <= 0.0000001

# <codecell>

def area_triangle(a,b,c):
    return abs( (a.x*(b.y-c.y) + b.x*(c.y-a.y) + c.x*(a.y-b.y))) / 2.0
assert area_triangle(P(0,0), P(0,1), P(1,0))
assert area_triangle(P(6,27), P(44,17), P(33,-13)) - 625 == 0

# <codecell>

def f_top_arc(x,C,r):  
    """ @param x independent var
        @param C circle mid point
        @param r radius
    """
    try:
        y = C.y + ( sqrt(r**2-(x-C.x)**2) )
    except:
        y = 0.       
    return y
rng=arange(0,4.,0.01)
plt.figsize(10,5)
plot(map(lambda x:f_top_arc(x,P(2,0),2),rng))

# <codecell>

f_bottom_arc=lambda x,C,r:  (C.y - ( sqrt(r**2-(x-C.x)**2) ))
rng=arange(0,2,0.0001)
plt.figsize(5,5)
plot(map(lambda x:f_bottom_arc(x,P(1,1),1),rng))

# <codecell>

Image(url='http://upload.wikimedia.org/math/4/8/3/483efae2397ac62560aa6f61d4e2e830.png')

# <codecell>

def integrate_arc_top(C, r, a, b):
    return quad( lambda z: f_top_arc (z,C,r) , a , b  ) [0] 

def integrate_arc_bottom(C, r, a, b):
    return quad( lambda z: f_bottom_arc (z,C,r) , a , b  ) [0] 

def volume_integrate_arc_top(C, r, a, b):
    return pi * ( quad( lambda z: (f_top_arc (z,C,r)**2) , a , b  ) [0] )

def volume_integrate_arc_bottom(C, r, a, b):
    return pi * ( quad( lambda z: (f_bottom_arc (z,C,r)**2) , a , b  ) [0] )

def vol_sphere(r):
    return (4./3.) * pi * (r ** 3)

res_top=volume_integrate_arc_top( P(-1,0), 1. , -2, 0)
res_bottom=volume_integrate_arc_bottom( P(-1,0), 1., -2, 0)
print vol_sphere(1),'vs',res_top
print res_bottom

res2_top=volume_integrate_arc_top( P(-1,0), 2. , -3, 1)
res2_bottom=volume_integrate_arc_bottom( P(-1,0), 2., -3, 1)
print 'r2=',res2_top,res2_bottom
print 'sphere(2)=',vol_sphere(2)

# <codecell>

def integrate_rectangle(R,a,b):
    return pi * (R**2)*abs(a-b)
assert abs(integrate_rectangle(1,0,1)-pi) <= 0.00001

# <codecell>

x=sympy.Symbol('x')
eq=(1 - ( sympy.sqrt(1-(x-1)**2) ))
sympy.integrate(eq)

# <codecell>


