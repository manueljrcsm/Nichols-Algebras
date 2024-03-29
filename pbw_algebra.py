# -*- coding: utf-8 -*-

import pbw_element as pe
import letters as l
import universe as u
import word as w
from counter import Counter
from collections import namedtuple

try:
    from sage.combinat.q_analogues import q_factorial, q_int
except:
    print('Sage modules q_factorial and/or q_int not found')
from free_algebra import FreeAlgebra

class PBWAlgebra(FreeAlgebra):
    """Where the PBW algebra lives. The computation of the relations is to be done in this class.
    """

    def __init__(self, string_pbw_generators: str,pbw_definitions: list, mother_algebra) -> None:
        # super().__init__(mother_algebra.string_generators, mother_algebra.base_field,
        # mother_algebra.q_matrix)
        string_to_list = string_pbw_generators.split(' ')
        if len(string_to_list) == len(pbw_definitions):
            PBWGeneratorsTuple = namedtuple('GeneratorsTuple', string_pbw_generators)
            self.pbw_generators = PBWGeneratorsTuple._make([l.PBWLetter(string_to_list[i],pbw_definitions[i]) for i in
                                                            range(len(pbw_definitions))])
        else:
            raise ValueError("The number of handles does not match the number of definitions provided.")
        u.Universe.pbw_generators = self.pbw_generators
        self.mother_algebra = mother_algebra
        #self.string_generators = mother_algebra.string_generators
        self.generators = mother_algebra.generators
        self.base_field = mother_algebra.base_field
        self.q_matrix = mother_algebra.q_matrix
        self.relations = {}  # No relations to begin with, updated with compute_relations below.
        self.compute_relations()
        
        for handle, val in self.relations.items():
            print("handle: ", handle, "val: ", val)
        u.Universe.set_pbw_universe(self)


    def compute_relations(self):
        """Append all the relations to the dictionary 'relations'."""  # TODO
        relations = u.Universe.relations # Create an alias to unburden notation.
        for i in range(len(self.pbw_generators)-1):
            for j in range(i+1,len(self.pbw_generators)):
                x_i: l.PBWLetter  = self.pbw_generators[i]
                x_j: l.PBWLetter = self.pbw_generators[j]
                trigger = (x_i,x_j) # The non-PBW term.
                q_ij = x_i.as_Word().q_bilinear(x_j.as_Word())

                target = w.Word([x_j,x_i])
                writing_rule = pe.PBWElement({target: q_ij}) # The right hand side
                # of the relation is initialized with the PBW-term of the bracket commutator
                """ SEARCH PATTERN GOES HERE, ADDING SUMMANDS TO writing_rule """
                target_degree = target.degree
                c = Counter(i, j, target_degree)
                while not c.out_of_bounds:
                    try:
                        candidate = w.Word([self.pbw_generators[j - n] for n in range(j - i + 1) for m in range(c.counter[n])])
                        if all(candidate.degree[letter] <= target_degree[letter] for letter in target_degree.keys()):
                            if any(candidate.degree[letter] < target_degree[letter] for letter in
                                   target_degree.keys()): # Case smaller degree.
                                c.increment()
                            else: # Case equal degree.
                                v = pe.PBWElement({candidate:1}).as_Element()
                                coeff = pe.PBWElement({target:1}).as_Element().c_bilinear(v) / v.c_bilinear(v) # Compute c_ij^candidate
                                writing_rule += pe.PBWElement({candidate: coeff})
                                c.round_up()
                        else: # Case greater degree.
                            c.round_up()
                    except KeyError:
                        c.increment()
                self.relations[trigger] = writing_rule
        """
        p = self.q_matrix[(Universe.generators[0], Universe.generators[0])]
        q = self.q_matrix[(Universe.generators[0], Universe.generators[1])]
        r = self.q_matrix[(Universe.generators[1], Universe.generators[1])]
        t = self.pbw_generators[0]
        z = self.pbw_generators[5]
        u = self.pbw_generators[1]
        import word as w
        self.relations[(z,t)] = pbw_element.PBWElement({w.Word([t,z]): q, w.Word([u]): 1})"""

