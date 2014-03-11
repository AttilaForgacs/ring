#coding: utf-8
from __future__ import division
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
from models import *


# l|r|t|b left right top bottom b|s big small c=circle
# C=center
# X,Y independent
# R=radius
# W=width H=height
# RI=inner ring radius


profiles_definiton = load_profiles_lookup_table({})

for i in [6]:
    ring_config = RingParams(W=6.0, H=2., CF=64., PROFILE='PR_0%02d'%i)
    ring_config.lookup_definition(profiles_definiton)

    # override ########
    # ring_config.W = 2.5
    # ring_config.H = 1.
    # ring_config.R60 = 0.
    # ring_config.R61 = 0.
    # ring_config.R40 = 0.5
    # ring_config.R20 = ring_config.R41 = 0.20


    print 'Using configuration:'
    print ring_config

    context = Context()
    model = globals()[ring_config.MODEL](params=ring_config, context=context)
    model.calculate_intersections()

    print context
    print 'vars:'
    print model.context.variables
    print
    print
    print 'eq:'
    print model.context.equations
    print
    print

    solutions = model.solve()

    print solutions

    volume = model.get_volume()

    print 'Volume:', volume

    from pylab import *

    plt.savefig('/home/attila/Desktop/RING_0%02d.png'%i)
    plt.clf()
    plt.close()