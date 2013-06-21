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

plt.show()

# <codecell>

%run?

# <codecell>

{
 "metadata": {
  "name": "integral"
 },
 "nbformat": 3,
 "nbformat_minor": 0,
 "worksheets": [
  {
   "cells": [
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "from collections import *\n",
      "from math import *\n",
      "from numpy import array, cos, sin\n",
      "from pylab import *\n",
      "import functools\n",
      "import scipy\n",
      "import sympy\n",
      "P = namedtuple('Point', ['x', 'y']);\n",
      "def area_rectangle_tl_br(tl,br):\n",
      "    return abs(tl.x-br.x) * abs(tl.y-br.y)\n",
      "from IPython.display import Image\n",
      "from scipy.integrate import quad\n",
      "#degrees = 180 * radians / pi\n",
      "#radians = pi * degrees / 180\n",
      "%pylab\n",
      "%load_ext sympy.interactive.ipythonprinting\n",
      "from decimal import *\n",
      "def assert_floats_equal(a,b):\n",
      "    return Decimal(a) == Decimal(b)\n"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "stream",
       "stream": "stdout",
       "text": [
        "\n",
        "Welcome to pylab, a matplotlib-based Python environment [backend: module://IPython.zmq.pylab.backend_inline].\n",
        "For more information, type 'help(pylab)'.\n"
       ]
      }
     ],
     "prompt_number": 15
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "def vector_length(pa,pb):\n",
      "    return sqrt( (pa.x - pb.x)**2 + (pa.y - pb.y)**2 )\n",
      "def get_angle_between_3_points(pc, p1, p2):\n",
      "    \"\"\" pc=point center, p1,p2 \"\"\"\n",
      "    vl = vector_length\n",
      "    return arccos ( ( vl(pc,p1)**2 + vl(pc,p2)**2 - vl(p1,p2)**2 ) / (2*vl(pc,p1)*vl(pc,p2)) )\n",
      "#get_angle_between_3_points( P(0,0), P(0,1), P(1,0)  )    "
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 3
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "def area_pie_slice(pc,p1,p2): \n",
      "    \"get area of circle-slice center(pc), 2 points on cirlce (p1,p2)\"\n",
      "    r = vector_length(pc,p1)\n",
      "    area_cirlce = (r*r)*pi\n",
      "    return area_cirlce * (get_angle_between_3_points(pc,p1,p2) / (2.*pi))  \n",
      "assert abs(   area_pie_slice ( P(0,0), P(0,1), P(1,0)  ) - pi/4   ) <= 0.0000001"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 5
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "def area_triangle(a,b,c):\n",
      "    return abs( (a.x*(b.y-c.y) + b.x*(c.y-a.y) + c.x*(a.y-b.y))) / 2.0\n",
      "assert area_triangle(P(0,0), P(0,1), P(1,0))\n",
      "assert area_triangle(P(6,27), P(44,17), P(33,-13)) - 625 == 0"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 6
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "f_top_arc=lambda x,C,r:  C.y + ( sqrt(r-(x-C.x)**2) )\n",
      "rng=arange(0,2,0.0001)\n",
      "figsize(5,5)\n",
      "plot(map(lambda x:f_top_arc(x,P(1,1),1),rng))"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "pyout",
       "prompt_number": 7,
       "text": [
        "[Line2D(_line0)]"
       ]
      },
      {
       "output_type": "display_data",
       "png": "iVBORw0KGgoAAAANSUhEUgAAAUcAAAE1CAYAAAB0oyKhAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz\nAAALEgAACxIB0t1+/AAAIABJREFUeJzt3XtcVVXeBvDnKGgiKozK0YBMwVDkZuqQGYbmLUu00NJK\nHdRiKHWcaZrqnbcE39Ka18nMyndq7KqlZpmWgHmZg1ekRrykU6GBgCgJioqOgrDeP9ZEKpuLcvZe\ne5/zfD8fPgrndNbv7I4Pa+299lo2IYQAERFdoZnqAoiIzIjhSESkgeFIRKSB4UhEpIHhSESkgeFI\nRKSh3nAsKCjAoEGD0KtXL4SFheG1116r9Zxly5YhMjISERERGDBgAPbt26dbsURERrHVN8/x+PHj\nOH78OKKiolBeXo4+ffrg888/R8+ePWues3PnToSGhqJdu3ZIT09HcnIyMjMzDSmeiEgv9fYcO3Xq\nhKioKACAt7c3evbsiaKioiue079/f7Rr1w4AEB0djcLCQp1KJSIyTqPPOebl5SE7OxvR0dF1PmfJ\nkiUYOXKkUwojIlJKNMLZs2dFnz59xOrVq+t8zubNm0XPnj3FyZMnNR8HwC9+8YtfunzpocFXraio\nEMOGDRMLFiyo8zl79+4VQUFBIicnp+6GdHoDVjZ79mzVJZgSj4s2HhdtemVLvcNqIQSmTp2K0NBQ\nzJo1S/M5+fn5uP/++7F06VIEBwfX93JERJbhUd+D27dvx9KlSxEREYHevXsDAObOnYv8/HwAQGJi\nIubMmYNTp04hKSkJAODp6YmsrCydyyYi0le9U3mc2pDNBoOasgyHw4HY2FjVZZgOj4s2HhdtemUL\nw5GILE2vbOHtg0REGhiOREQaGI5ERBoYjkREGhiOREQaGI5ERBoYjkREGhiOREQaGI5ERBoYjkRE\nGhiOREQaGI5ERBoYjkREGhiOREQaGI5ERBoYjkREGhiOREQaGI5ERBoYjkREGhiOREQaGI5ERBoY\njkREGhiOREQaGI5ERBoYjkREGhiOREQaGI5ERBoYjkREGhiOREQaGI5ERBoYjkREGhiOREQaGI5E\nRBoYjkREGhiOREQaGI5ERBoYjkREGuoNx4KCAgwaNAi9evVCWFgYXnvtNc3nzZw5E927d0dkZCSy\ns7N1KZSIyEge9T3o6emJBQsWICoqCuXl5ejTpw+GDh2Knj171jwnNTUVhw4dQk5ODnbt2oWkpCRk\n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\nTkSuQmCC\n"
      }
     ],
     "prompt_number": 7
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "f_bottom_arc=lambda x,C,r:  (C.y - ( sqrt(r-(x-C.x)**2) ))\n",
      "rng=arange(0,2,0.0001)\n",
      "figsize(5,5)\n",
      "plot(map(lambda x:f_bottom_arc(x,P(1,1),1),rng))"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "output_type": "pyout",
       "prompt_number": 8,
       "text": [
        "[Line2D(_line0)]"
       ]
      },
      {
       "output_type": "display_data",
       "png": "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\nhDegY9RGJ1IAAAAASUVORK5CYII=\n"
      }
     ],
     "prompt_number": 8
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "Image(url='http://upload.wikimedia.org/math/4/8/3/483efae2397ac62560aa6f61d4e2e830.png')"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "html": [
        "<img src=\"http://upload.wikimedia.org/math/4/8/3/483efae2397ac62560aa6f61d4e2e830.png\" />"
       ],
       "output_type": "pyout",
       "prompt_number": 9,
       "text": [
        "<IPython.core.display.Image object at 0x4018490>"
       ]
      }
     ],
     "prompt_number": 9
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "def integrate_arc_top(C, r, a, b):\n",
      "    return pi * ( quad( lambda z: f_top_arc (z,C,r)**2 , a , b  ) [0] )\n",
      "def integrate_arc_bottom(C, r, a, b):\n",
      "    return pi * ( quad( lambda z: f_bottom_arc (z,C,r)**2 , a , b  ) [0] )\n",
      "assert integrate_arc_top( P(2,0), 1, 2,3 ) - ((4./3.)*pi/2) <= 0 # half sphere\n",
      "assert integrate_arc_bottom( P(2,0), 1, 2,3 ) - ((4./3.)*pi/2) <= 0 # half sphere"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 17
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "def integrate_rectangle(R,a,b):\n",
      "    return pi * (R**2)*abs(a-b)\n",
      "assert abs(integrate_rectangle(1,0,1)-pi) <= 0.00001"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [],
     "prompt_number": 18
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [
      "x=sympy.Symbol('x')\n",
      "eq=(1 - ( sympy.sqrt(1-(x-1)**2) ))\n",
      "sympy.integrate(eq)"
     ],
     "language": "python",
     "metadata": {},
     "outputs": [
      {
       "latex": [
        "$$x - \\begin{cases} \\frac{\\mathbf{\\imath} \\left(x -1\\right)^{3}}{2 \\sqrt{\\left(x -1\\right)^{2} -1}} - \\frac{\\mathbf{\\imath} \\left(x -1\\right)}{2 \\sqrt{\\left(x -1\\right)^{2} -1}} - \\frac{1}{2} \\mathbf{\\imath} \\operatorname{acosh}{\\left (x -1 \\right )} & \\text{for}\\: \\lvert{\\left(x -1\\right)^{2}}\\rvert > 1 \\\\- \\frac{\\left(x -1\\right)^{3}}{2 \\sqrt{- \\left(x -1\\right)^{2} + 1}} + \\frac{x -1}{2 \\sqrt{- \\left(x -1\\right)^{2} + 1}} + \\frac{1}{2} \\operatorname{asin}{\\left (x -1 \\right )} & \\text{otherwise} \\end{cases}$$"
       ],
       "output_type": "pyout",
       "prompt_number": 19,
       "text": [
        "    \u23a7               3                                                         \n",
        "    \u23aa      \u2148\u22c5(x - 1)             \u2148\u22c5(x - 1)        \u2148\u22c5acosh(x - 1)        \u2502     \n",
        "x - \u23aa \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 - \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 - \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500    for \u2502(x - \n",
        "    \u23aa      ______________        ______________         2                     \n",
        "    \u23aa     \u2571        2            \u2571        2                                    \n",
        "    \u23aa 2\u22c5\u2572\u2571  (x - 1)  - 1    2\u22c5\u2572\u2571  (x - 1)  - 1                                \n",
        "    \u23a8                                                                         \n",
        "    \u23aa                3                                                        \n",
        "    \u23aa         (x - 1)                  x - 1           asin(x - 1)            \n",
        "    \u23aa- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 + \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 + \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500      otherw\n",
        "    \u23aa       ________________        ________________        2                 \n",
        "    \u23aa      \u2571          2            \u2571          2                               \n",
        "    \u23a9  2\u22c5\u2572\u2571  - (x - 1)  + 1    2\u22c5\u2572\u2571  - (x - 1)  + 1                           \n",
        "\n",
        "        \n",
        "  2\u2502    \n",
        "1) \u2502 > 1\n",
        "        \n",
        "        \n",
        "        \n",
        "        \n",
        "        \n",
        "        \n",
        "ise     \n",
        "        \n",
        "        \n",
        "        "
       ]
      }
     ],
     "prompt_number": 19
    },
    {
     "cell_type": "code",
     "collapsed": false,
     "input": [],
     "language": "python",
     "metadata": {},
     "outputs": []
    }
   ],
   "metadata": {}
  }
 ]
}

# <codecell>

%load

# <codecell>


