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

INTEGRATE_STEP = 0.001
EPS = 1e-5 #epsilon for error checking
def test_eq(a,b):
    assert abs(a-b) <= EPS
    return True

# <codecell>

def vector_length(pa,pb):
    return sqrt( (pa.x - pb.x)**2 + (pa.y - pb.y)**2 )
def get_angle_between_3_points(pc, p1, p2):
    """ pc=point center, p1,p2 """
    vl = vector_length
    return arccos ( ( vl(pc,p1)**2 + vl(pc,p2)**2 - vl(p1,p2)**2 ) / (2*vl(pc,p1)*vl(pc,p2)) )
#get_angle_between_3_points( P(0,0), P(0,1), P(1,0)  )    

# <codecell>

def f_line(x,h):  
    return h

# <codecell>

def f_slope(x,x1,y1,x2,y2):
    """
    y = y1 + [(y2 - y1) / (x2 - x1)]·(x - x1)
    """
    return y1 + ( (y2-y1) / (x2-x1) ) * (x-x1)

Image(url="http://upload.wikimedia.org/math/b/a/6/ba65ae69f70f05c690d155c5ad2f4379.png")    

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

#rng=arange(0,4.,0.01)
#plt.figsize(10,5)
#plot(map(lambda x:f_top_arc(x,P(2,0),2),rng))

# <codecell>

f_bottom_arc=lambda x,C,r:  (C.y - ( sqrt(r**2-(x-C.x)**2) ))

    
#rng=arange(0,2,0.0001)
#plt.figsize(5,5)
#plot(map(lambda x:f_bottom_arc(x,P(1,1),1),rng))

# <codecell>

Image(url='http://upload.wikimedia.org/math/4/8/3/483efae2397ac62560aa6f61d4e2e830.png')

# <codecell>

def integrate_arc_top(C, r, a, b):
    return quad( lambda z: f_top_arc (z,C,r) , a , b  ) [0] 

def integrate_arc_bottom(C, r, a, b):
    return quad( lambda z: f_bottom_arc (z,C,r) , a , b  ) [0] 

def integrate_line(h,a,b):
    return quad( lambda z: f_line(z,h), a,b) [0]

def integrate_slope(x1,y1,x2,y2,a,b):
    return quad( lambda z: f_slope(z,x1,y1,x2,y2), a,b) [0]

def volume_integrate_arc_top(C, r, a, b):
    rng = arange(a,b,INTEGRATE_STEP)
    plot(rng,map(lambda z:f_top_arc(z,C,r), rng ))
    return pi * ( quad( lambda z: (f_top_arc (z,C,r)**2) , a , b  ) [0] )

def volume_integrate_arc_bottom(C, r, a, b):
    rng = arange(a,b,INTEGRATE_STEP)
    plot(rng,map(lambda z:f_bottom_arc(z,C,r), rng ))
    return pi * ( quad( lambda z: (f_bottom_arc (z,C,r)**2) , a , b  ) [0] )

def volume_integrate_line(h,a,b):
    rng = arange(a,b,INTEGRATE_STEP)
    plot(rng,map(lambda z:f_line(z,h), rng ))
    return pi * ( quad( lambda z: (f_line (z,h)**2) , a , b  ) [0] )

def volume_integrate_slope(x1,y1,x2,y2,a,b):
    rng = arange(a,b,INTEGRATE_STEP)
    plot(rng,map(lambda z:f_slope(z,x1,y1,x2,y2), rng ))
    return pi * ( quad( lambda z: (f_slope(z,x1,y1,x2,y2)**2) , a , b  ) [0] )
    
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

assert abs (integrate_line(10,0,10) - 100.) <= EPS
assert abs (volume_integrate_line(10,0,10) - 1000*pi) <= EPS
plt.clf()
assert abs (integrate_slope(0,0,10,10,0,10) - 50.) <= EPS
cohn = volume_integrate_slope(0,0,10,10,0,10)
kone = (1/3.) * pi * (10**2) * 10
test_eq(cohn,kone)
plt.clf()

# <codecell>

def integrate_rectangle(R,a,b):
    return pi * (R**2)*abs(a-b)
assert abs(integrate_rectangle(1,0,1)-pi) <= 0.00001

# <codecell>

x=sympy.Symbol('x')
eq=(1 - ( sympy.sqrt(1-(x-1)**2) ))
sympy.integrate(eq)

# <codecell>


