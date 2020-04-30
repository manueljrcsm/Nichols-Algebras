from typing import Dict, Iterable
import re
import letters as l
import element as e
import universe as u
import word as w
import numpy as np
from collections import namedtuple


class FreeAlgebra:
    """Where the free algebra itself lives. It serves a structure superclass for PBW_algebra."""

    def __init__(self, string_generators: str, roots_of_unity: Dict[str,tuple] ={},
                 q_matrix: Iterable[Iterable[str]] = None,  print_stats = False):        
        #STEP 1: CHECK THAT THE INPUT IS CONSISTENT
        
        
        seperator_string="[ , ;]" # characters which can be used to seperate letters
        generators_list = [gen for gen in re.split(seperator_string, string_generators) if gen != ""]
        
        #CHECK THAT NO GENERATOR IN THE GENERATOR STRING IS ALSO USED TO DENOTE SOME ROOT OF UNITY
        for gen in generators_list:
            if gen in roots_of_unity:
                msg ="It is not allowed to use the same variable names for the generators and constants in the field."
                raise AssertionError(msg)
              
        if type(q_matrix)!= np.matrix:
            q_matrix = np.matrix([[1 for x in generators_list] for y in generators_list])
                  
        if not q_matrix.shape == (len(generators_list), len(generators_list)):

            msg = "The matrix has the wrong dimensions. Expected ({2},{2}), but got ({0},{1}).".format(
                q_matrix.shape[0], q_matrix.shape[1], len(self.generators))
            raise AssertionError(msg)
                             
        #TO BE ADAPTED TO THE SAGE TERMINOLOGY 
        try:
            from sage.all_cmdline import UniversalCyclotomicField  # imports sage library      
            P = UniversalCyclotomicField()       
        except ModuleNotFoundError:  # IGNORE
            msg = "Couldn't setup the cyclotomic number field. Please make sure that Sage can be used."
            raise AssertionError(msg)
            
        u.Universe.set_constants()
        
        GeneratorsTuple = namedtuple('GeneratorsTuple', " ".join([gen for gen in generators_list]) )             
        #object.__setattr__(self,"generators",{ gen: l.Letter(gen, print_stats) for gen in generators_list})
        object.__setattr__(self,"generators", GeneratorsTuple._make([l.Letter(gen, print_stats) for gen in generators_list]))
        object.__setattr__(self, "base_field", P)
        object.__setattr__(self, "field_variables_dict",
                           {name: self.base_field.gen(roots_of_unity[name][0], roots_of_unity[name][1]) 
                            for name, val in roots_of_unity.items()}
                           )
        object.__setattr__(self, "q_matrix",
                           {(self.generators[row],
                             self.generators[col]):
                            self.field_variables_dict[q_matrix[row, col]] 
                            for row in range(len(generators_list)) 
                            for col in range(len(generators_list))})
        """    
        object.__setattr__(self, "q_matrix",
                           {(list(self.generators.values())[row],
                             list(self.generators.values())[col]):
                            self.field_variables_dict[q_matrix[row, col]] 
                            for row in range(len(generators_list)) 
                            for col in range(len(generators_list))})
        """
        #TODO: STRING PARSER FOR MORE COMPLICATED INPUTS NECESSARY
        u.Universe.set_universe(self)
        
        if print_stats:
            print("A free algebra with %s generators over the algebraic closure of Q is being generated." 
                  % len(generators_list))

        
    def create_pbw_letter(self, handle: str, presentation: e.Element):
        return l.PBWLetter(handle, presentation, True)
    
    def bracket(self, first, second) -> e.Element:
        """ Computes the q-commutator bracket [first, second]_q of elements. This function splits the commutator
        linearly in the factors and calls word_bracket on pairs of Words (i.e., homogenous components)."""
        # TODO verify
        if type(first) == l.Letter:
            internal_first = e.Element({w.Word([first]) :1 })
        elif type(first) == l.PBWLetter:
            internal_first = first.presentation
        elif type(first) == w.Word:
            internal_first = e.Element({first :1 })
        elif type(first) == e.Element:
            internal_first = first
        else:
            msg = "Unallowed input type for to commpute the skew-bracket."
            raise AssertionError(msg)
            
        if type(second) == l.Letter:
            internal_second = e.Element({w.Word([second]) :1 })
        elif type(second) == l.PBWLetter:
            internal_second = second.presentation
        elif type(second) == w.Word:
            internal_second = e.Element({second :1 })
        elif type(second) == e.Element:
            internal_second = second
        else:
            msg = "Unallowed input type for to commpute the skew-bracket."
            raise AssertionError(msg)
            
        result = u.Universe.ElementZERO
        for term_1, sca_1 in internal_first.pairs:
            for term_2, sca_2 in internal_second.pairs:
                result += self.word_bracket(term_1,term_2).scalar_multiply(sca_1*sca_2)
    
        return result


    def word_bracket(self, word1: w.Word, word2: w.Word) -> e.Element:

        """Computes the bracket [word1,word2]_q between homogeneous components."""
        first = e.Element({word1: 1})
        second = e.Element({word2: 1})
        return first*second - (second*first).scalar_multiply(word1.q_bilinear(word2))

   
    def get_element(self, input_string, scalar=1):
        x = u.Universe.type_conversion(self.generators[input_string], e.Element)
        print(x)

        try:
            return u.Universe.type_conversion(self.generators[input_string], e.Element).scalar_multiply(scalar)
        except:
            print("No such letter exists.")
            return None
    
    def set_element(self, string, scalar) -> e.Element:
        """The most pratical way to construct a new element. Constructs individual monomials (with an optional scalar).
        Inputs: string, scalar (one by default).
        Output: element of the form 'scalar times string' written in the PBW basis.
        """
        if string == 0:
            newelement = u.Universe.ElementZERO
        else:
            newelement = e.Element({string: scalar})
        return newelement.rewrite()
    
    #def set_pbw_generator(self, handle: str, representation) -> letters.PBWLetter:
    #    """Creates the PBW generator with a given handle and representation."""

    #    return letters.PBWLetter(handle, representation)
                    
        


# STATIC OBJECTS OF ELEMENT
# TODO create a subclass to make them immutable by overriding __setattr__ and #  __delattr__ ?
# see https://stackoverflow.com/questions/2682745/how-do-i-create-a-constant-in-python/59935007#59935007
# or maybe https://stackoverflow.com/questions/24876364/define-a-constant-object-in-python

"""
def create_element(string, scalar=1):
"""
"""The most pratical way to construct a new element. Constructs individual monomials (with an optional scalar).
Inputs: string, scalar (one by default).
Output: element of the form 'scalar times string' written in the PBW basis.
"""
""" 
if string == 0:
    newelement = Element({'': 0})
else:
    newelement = Element({string: scalar})
return newelement.rewrite()
"""
"""
def bracket(first: Element, second: Element) -> Element:
"""  
""" Computes the q-commutator bracket [first, second]_q of elements. This function splits the commutator
linearly in the factors and calls word_bracket on pairs of Words (i.e., homogenous components)."""
# TODO verify
"""  
result = u.Universe.ElementZERO
for term_1, sca_1 in first.pairs:
    for term_2, sca_2 in second.pairs:
        result += word_bracket(term_1,term_2).scalar_multiply(sca_1*sca_2)

return result
"""
"""
def word_bracket(word1: w.Word, word2: w.Word) -> Element:
"""  
"""Computes the bracket [word1,word2]_q between homogeneous components."""
"""  
first = Element({word1: 1})
second = Element({word2: 1})
return first*second - (second*first).scalar_multiply(word1.q_bilinear(word2))
"""



