# -*- coding: utf-8 -*-

import numpy as np

from free_algebra import FreeAlgebra
from pbw_element import PBWElement

try:
    from sage.combinat.q_analogues import q_factorial, q_int
except:
    print('Sage module not found')
from element import Element

pbw_generators = ('x', 'y')


class PBWAlgebra:
    """Where the PBW algebra lives. The computation of the relations is to be done in this class.
    """

    def __init__(self, pbw_generators: str, free_algebra: FreeAlgebra) -> None:
        self.free_algebra = free_algebra
        self.pbw_generators = pbw_generators
        self.relations = {}  # No relations to begin with, updated with compute_relations below.
        self.compute_relations()

    def set_pbw_element(self, string: str, scalar) -> PBWElement:
        """The most pratical way to construct a new element. Constructs individual monomials (with an optional scalar).
        Inputs: string, scalar (one by default).
        Output: pbw_element of the form 'scalar times string' written in the PBW basis.
        """
        if string == 0:
            newelement = PBWElement({'': 0})
        else:
            newelement = PBWElement({string: scalar})
        return newelement.rewrite()

    def compute_relations(self):
        """Append all the relations to the dictionary 'relations'"""  # TODO


def degree(word):
    deg = np.zeros(len(pbw_generators), dtype=int)
    for letter in word:
        for generator in pbw_generators:
            if letter == generator:
                index = pbw_generators.index(generator)
                deg[index] += 1
                break
    return deg  # in Z^2
