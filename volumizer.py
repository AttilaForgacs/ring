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
ring_config = RingParams(W=5., H=1.5, CF=56., PROFILE='PR_001')
ring_config.lookup_definition(profiles_definiton)

# override ########
ring_config.W = 2.5
ring_config.H = 1.
ring_config.R60 = 0.
ring_config.R61 = round(2.17718474478179, 3)
ring_config.R40 = round(0.35,3)
ring_config.R41 = round(0.455863932713471,3)


print 'Using configuration:'
print ring_config

context = Context()
model = globals()[ring_config.MODEL](params=ring_config, context=context)
model.create_equations()

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
