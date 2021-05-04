import numpy as np

from rng.mrg32k3a import MRG32k3a
from oracles.mm1queue import MM1Queue
from oracles.cntnv import CntNV  # names of .py file and Oracle subclass
from oracles.facilitysizing import FacilitySize
from base import Solution

fixed_factors = {}
myoracle = FacilitySize(fixed_factors)
print(myoracle.factors)

mysoln_factors = {}

# Check simulatability
for key in fixed_factors:
    print(key, myoracle.check_simulatable_factor(key))

myoracle.factors.update(mysoln_factors)
print(myoracle.factors)
for key in mysoln_factors:
    print(key, myoracle.check_simulatable_factor(key))

print(myoracle.check_simulatable_factors())

# print('For x = (1,), is_simulatable should be True and is {}'.format(myoracle.check_simulatable_factor(x=(1,))))
# print('For x = [1], is_simulatable should be True(?) and is {}'.format(myoracle.check_simulatable_factor(x=(1,))))
# print('For x = (-1,), is_simulatable should be False and is {}'.format(myoracle.check_simulatable_factor(x=(-1,))))
# print('For x = (0,), is_simulatable should be False and is {}'.format(myoracle.check_simulatable_factor(x=(0,))))
# print('For x = (1,2), is_simulatable should be False and is {}'.format(myoracle.check_simulatable_factor(x=(1,2))))
# print('For x = "hi", is_simulatable should be False and is {}'.format(myoracle.check_simulatable_factor(x='hi')))

rng_list = [MRG32k3a() for _ in range(myoracle.n_rngs)]
# print(rng_list)
# mysolution.attach_rngs(rng_list)
# print(mysolution.rng_list)


# Test replicate()
responses, gradients = myoracle.replicate(rng_list)
print('For a single replication:')
print('The responses are {}'.format(responses))
print('The gradients are {}'.format(gradients))
