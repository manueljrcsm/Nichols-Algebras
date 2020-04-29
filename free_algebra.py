
import re
import letters
from typing import Dict, Iterable
import element
import word
from universe import Universe
import numpy as np
from letters import Letter
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

            msg = "The matrix has the wrong dimensions. Expected ({2},{2}), but got ({2},{2}).".format(
                q_matrix.shape[0], q_matrix.shape[1], len(self.generators))
            raise AssertionError(msg)
                             
        #TO BE ADAPTED TO THE SAGE TERMINOLOGY 
        try:
            from sage.all_cmdline import UniversalCyclotomicField  # imports sage library      
            P = UniversalCyclotomicField()       
        except ModuleNotFoundError:  # IGNORE
            msg = "Couldn't setup the cyclotomic number field. Please make sure that Sage can be used."
            raise AssertionError(msg)
                       
        if print_stats:
            print("A free algebra with %s generators over the algebraic closure of Q is being generated." 
                  % len(generators_list))    
            
        object.__setattr__(self,"generators",{ gen: letters.Letter(gen, print_stats) for gen in generators_list})
        object.__setattr__(self, "base_field", P)
        object.__setattr__(self, "field_variables_dict",
                           {name: self.base_field.gen(roots_of_unity[name][0], roots_of_unity[name][1]) 
                            for name, val in roots_of_unity.items()}
                           )
        object.__setattr__(self, "q_matrix",
                           {(list(self.generators.values())[row],
                             list(self.generators.values())[col]):
                            self.field_variables_dict[q_matrix[row, col]] 
                            for row in range(len(generators_list)) 
                            for col in range(len(generators_list))})
        #TODO: STRING PARSER FOR MORE COMPLICATED INPUTS NECESSARY
        
        Universe.set_universe(self)       
        
    def create_pbw_letter(self, handle: str, presentation: element.Element):
        return letters.PBWLetter(handle, presentation, True)
    
    def bracket(self, first, second) -> element.Element:
        """ Computes the q-commutator bracket [first, second]_q of elements. This function splits the commutator
        linearly in the factors and calls word_bracket on pairs of Words (i.e., homogenous components)."""
        # TODO verify
        if type(first) == letters.Letter:
            internal_first = element.Element({word.Word([first]) :1 })
        elif type(first) == letters.PBWLetter:
            internal_first = first.presentation
        elif type(first) == word.Word:
            internal_first = element.Element({first :1 })
        elif type(first) == element.Element:
            internal_first = first
        else:
            msg = "Unallowed input type for to commpute the skew-bracket."
            raise AssertionError(msg)
            
        if type(second) == letters.Letter:
            internal_second = element.Element({word.Word([second]) :1 })
        elif type(second) == letters.PBWLetter:
            internal_second = second.presentation
        elif type(second) == word.Word:
            internal_second = element.Element({second :1 })
        elif type(second) == element.Element:
            internal_second = second
        else:
            msg = "Unallowed input type for to commpute the skew-bracket."
            raise AssertionError(msg)
            
        result = element.ElementZERO
        for term_1, sca_1 in internal_first.pairs:
            for term_2, sca_2 in internal_second.pairs:
                result += self.word_bracket(term_1,term_2).scalar_multiply(sca_1*sca_2)
    
        return result


    def word_bracket(self, word1: word.Word, word2: word.Word) -> element.Element:

        """Computes the bracket [word1,word2]_q between homogeneous components."""
        first = element.Element({word1: 1})
        second = element.Element({word2: 1})
        return first*second - (second*first).scalar_multiply(word1.q_bilinear(word2))

   
    def get_element(self, input_string, scalar=1):
        try:
            return self.generators[input_string].to_element().scalar_multiply(scalar)
        except:
            print("No such letter exists.")
            return None
    
    def set_element(self, string, scalar) -> element.Element:
        """The most pratical way to construct a new element. Constructs individual monomials (with an optional scalar).
        Inputs: string, scalar (one by default).
        Output: element of the form 'scalar times string' written in the PBW basis.
        """
        if string == 0:
            newelement = element.Element({'': 0})
        else:
            newelement = element.Element({string: scalar})
        return newelement.rewrite()
    
    #def set_pbw_generator(self, handle: str, representation) -> letters.PBWLetter:
    #    """Creates the PBW generator with a given handle and representation."""

    #    return letters.PBWLetter(handle, representation)
                    
        







