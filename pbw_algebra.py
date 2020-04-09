# -*- coding: utf-8 -*-

import numpy as np
import pbw_element
from letters import PBWLetter
from universe import Universe

try:
    from sage.combinat.q_analogues import q_factorial, q_int
except:
    print('Sage module not found')
from free_algebra import FreeAlgebra

class PBWAlgebra(FreeAlgebra):
    """Where the PBW algebra lives. The computation of the relations is to be done in this class.
    """

    def __init__(self, string_pbw_generators: str,pbw_definitions: list, mother_algebra) -> None:
        # super().__init__(mother_algebra.string_generators, mother_algebra.base_field,
            # mother_algebra.q_matrix)
        string_to_list = string_pbw_generators.split(' ')
        if len(string_to_list) == len(pbw_definitions):
            self.pbw_generators = [PBWLetter(string_to_list[i],pbw_definitions[i]) for i in range(len(pbw_definitions))]

        self.mother_algebra = mother_algebra
        self.string_generators = mother_algebra.string_generators
        self.generators = mother_algebra.string_generators
        self.base_field = mother_algebra.base_field
        self.q_matrix = mother_algebra.q_matrix
        self.relations = {}  # No relations to begin with, updated with compute_relations below.
        self.compute_relations()
        Universe.set_pbw_universe(self)

    def set_pbw_element(self, string: str, scalar = 1):
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
        """Append all the relations to the dictionary 'relations'."""  # TODO
        p = self.q_matrix[(Universe.generators[0], Universe.generators[0])]
        q = self.q_matrix[(Universe.generators[0], Universe.generators[1])]
        r = self.q_matrix[(Universe.generators[1], Universe.generators[1])]
        self.relations['zt'] = pbw_element.PBWElement({'tz': q, 'u': 1})
        self.relations['zu'] = pbw_element.PBWElement({'uz': p*q, 'x': 1})
        self.relations['zx'] = pbw_element.PBWElement({'xz': p*p*q, 'y': 1})
        self.relations['xu'] = pbw_element.PBWElement({'ux': p*p*q*q*q*r, 'v': 1})
        self.relations['zy'] = pbw_element.PBWElement({'yz': p*p*p*q})
        self.relations['ut'] = pbw_element.PBWElement({'tu': (1 + r - r*q*q)/(q*r), 'ttz': (1 - q*q)*(1 - q*q*r)/(q*q*r)})
