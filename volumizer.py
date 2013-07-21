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
ring_config = RingParams(W=6., H=1.8, CF=56., PROFILE='PR_007')
ring_config.lookup_definition(profiles_definiton)

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
