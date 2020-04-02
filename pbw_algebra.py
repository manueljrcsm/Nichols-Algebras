# -*- coding: utf-8 -*-

import numpy as np

from free_algebra import Free_Algebra

try:
    from sage.combinat.q_analogues import q_factorial, q_int
except:
    print('Sage module not found')
from element import element

pbw_generators = ('x', 'y')


class PBW_algebra:
    """Where the PBW algebra lives. The computation of the relations is to be done in this class.
    """
    def __init__(self, pbw_generators, free_algebra: Free_Algebra) -> None:
        self.free_algebra = free_algebra
        self.pbw_generators = pbw_generators
        self.relations = {} # No relations to begin with, updated with compute_relations below.

    def compute_relations(self):
        """Append all the relations to the dictionary 'relations'"""




def degree(word):
    deg = np.zeros(len(pbw_generators), dtype=int)
    for letter in word:
        for generator in pbw_generators:
            if letter == generator:
                index = pbw_generators.index(generator)
                deg[index] += 1
                break
    return deg  # in Z^2


# Consider importing sage.combinat.q_analogues.q_int outside of Anaconda (running via a SAGE Jupyter Notebook),
# similar for q_factorial.
def q_int(n: int, q):
    # only works with 
    result = 0
    for i in range(n):
        result += q**i
    return result


def q_factorial(n: int, q):
    result = 1
    for i in range(n):
        result *= q_int(i + 1, q)
    return result


def q_bilinear(first: element, second: element):
    return
