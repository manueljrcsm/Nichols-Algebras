# -*- coding: utf-8 -*-
import re
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
        
        print(" ".join([str(self.pbw_generators[i].handle)+ str(self.pbw_generators[i].degree) for i in range(len(pbw_definitions)) ]))        
        
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
                
                #DEBUG
                print("Computing relations between ", x_i, " and ", x_j)
                
                trigger = (x_i,x_j) # The non-PBW term.
                q_ij = x_i.as_Word().q_bilinear(x_j.as_Word())

                target = w.Word([x_j,x_i])
                writing_rule = pe.PBWElement({target: q_ij}) # The right hand side
                # of the relation is initialized with the PBW-term of the bracket commutator
                """ SEARCH PATTERN GOES HERE, ADDING SUMMANDS TO writing_rule """
                target_degree = target.degree
                
                c = Counter(i, j, target_degree)
                
                while not c.out_of_bounds:
                    current_state = c.state()
                    if current_state < 0:
                        c.increment()
                        
                    elif current_state == 0:
                        
                        candidate = w.Word([self.pbw_generators[j-n] for n in range(j - i + 1) for m in range(c.counter[-(n+1)])])
                        if not candidate == target: # Excluding the target case. See Lemma 4.5
                            
                            v = pe.PBWElement({candidate:1})    
                            norm_v = v.c_bilinear(v)
                            if norm_v != 0:
                                coeff = pe.PBWElement({w.Word([x_i,  x_j]):1}).c_bilinear(v) / norm_v # Compute c_ij^candidate
                            else:
                                 msg = ("The orthogonality condition of the c-bilinear form was not met."+
                                 " Please check the given pbw generators and the matrix of the braiding. ")
                                 raise AssertionError(msg)
                            print("Found the candidate: ", v, " with coeff: ", coeff)
                            print("   ", c.counter)
                            if coeff != 0:
                                writing_rule += pe.PBWElement({candidate: coeff})
                        c.round_up()
                                    
                    else:
                        c.round_up()      
                
                self.relations[trigger] = writing_rule
                print("Found the relation ", x_i, x_j," = ", writing_rule)
        """
        p = self.q_matrix[(Universe.generators[0], Universe.generators[0])]
        q = self.q_matrix[(Universe.generators[0], Universe.generators[1])]
        r = self.q_matrix[(Universe.generators[1], Universe.generators[1])]
        t = self.pbw_generators[0]
        z = self.pbw_generators[5]
        u = self.pbw_generators[1]
        import word as w
        self.relations[(z,t)] = pbw_element.PBWElement({w.Word([t,z]): q, w.Word([u]): 1})"""

    def get_PBWElement(self, input_string):
        
        seperator_string="[ , ;]" # characters which can be used to seperate letters
        input_list = [inp for inp in re.split(seperator_string, input_string) if inp != ""]
        return pe.PBWElement({w.Word([getattr(self.pbw_generators, inp) for inp in input_list]):1})
        