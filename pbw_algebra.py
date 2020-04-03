# -*- coding: utf-8 -*-

import numpy as np
from config import *


import pbw_element

pbw_generators = ('x', 'y')
from free_algebra import FreeAlgebra

class PBWAlgebra(FreeAlgebra):
    """Where the PBW algebra lives. The computation of the relations is to be done in this class.
    """

    def __init__(self, string_pbw_generators: str, mother_algebra) -> None:
        super().__init__(mother_algebra.string_generators, mother_algebra.base_field, mother_algebra.variables,
            mother_algebra.q_matrix)
        self.pbw_generators = string_pbw_generators.split(' ')
        self.mother_algebra = mother_algebra
        self.relations = {}  # No relations to begin with, updated with compute_relations below.
        self.compute_relations()
        pbw_element.PBWElement.set_universe(self)

    def set_pbw_element(self, string: str, scalar):
        """The most pratical way to construct a new element. Constructs individual monomials (with an optional scalar).
        Inputs: string, scalar (one by default).
        Output: pbw_element of the form 'scalar times string' written in the PBW basis.
        """
        if string == 0:
            newelement = pbw_element.PBWElement({'': 0})
        else:
            newelement = pbw_element.PBWElement({string: scalar})
        return newelement.rewrite()

    def compute_relations(self):
        """Append all the relations to the dictionary 'relations'"""  # TODO
        print(self.variables)
        self.relations['zt'] = pbw_element.PBWElement({'tz': q, 'u': 1})
        self.relations['zu'] = pbw_element.PBWElement({'uz': p*q, 'x': 1})
        self.relations['zx'] = pbw_element.PBWElement({'xz': p*p*q, 'y': 1})
        self.relations['xu'] = pbw_element.PBWElement({'ux': p*p*q*q*q*r, 'v': 1})
        self.relations['zy'] = pbw_element.PBWElement({'yz': p*p*p*q})
        self.relations['ut'] = pbw_element.PBWElement({'tu': (1 + r - r*q*q)/(q*r), 'ttz': (1 - q*q)*(1 - q*q*r)/(q*q*r)})


def degree(word):
    deg = np.zeros(len(pbw_generators), dtype=int)
    for letter in word:
        for generator in pbw_generators:
            if letter == generator:
                index = pbw_generators.index(generator)
                deg[index] += 1
                break
    return deg  # in Z^2
