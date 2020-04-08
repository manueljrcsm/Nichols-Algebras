# -*- coding: utf-8 -*-

#import free_algebra
import tensor_element
import word

class Element:
    """Elements in the free algebra live here.
    """

    # Class attributes.
    universe = None
    base_field = None
    q_matrix = None
    generators = None
    variables = ()

    def __init__(self, dic):
        """
    Constructor. An object structure is stored in a dictionary. Defines some attributes of the element which can
            then be manipulated.
        """
        newdic = dic.copy()
        self.poly = newdic
        self.scalars = newdic.values()
        self.terms = newdic.keys()
        self.pairs = newdic.items()

    def __str__(self):
        """Creates the string representation of an element, i.e., what you see when you do '
        (element)'.
        """
        word = ""
        i = 0
        for term, sca in self.pairs:
            # Run through the monomial terms of the element.z
            scalar = str(sca)
            if scalar == "1" and str(term) != "":
                # If the coefficient of a term is 1, then it is ommited.
                scalar = ""
            if i > 0:
                # Adds a plus sign between consecutive terms.
                word += " + "
            if len(scalar) > 3 or scalar[0:1] == "-":
                # Terms with a minus sign or complicated elements from K are put under  parentheses, for clarity.
                scalar = "(" + scalar + ")"
            word += scalar + present(term)  # present does some eye-candy on the monomial string representation.
            i += 1
        if word == "":  # Empty dictionaries correspond to the 0 element.
            return "0"
        else:
            return word

    def __eq__(self, other):
        """Defines when two nichols elements are equal.

        I.e., when written in the basis, the monomial terms are all the same with the same coefficients.
        """
        newself = self.rewrite()
        newother = other.rewrite()
        for term1, sca1 in newself.pairs:
            if term1 not in newother.terms:
                return False
            elif sca1 != newother.poly[term1]:
                return False
        for term2, sca2 in newother.pairs:
            if term2 not in newself.terms:
                return False
            elif sca2 != newself.poly[term2]:
                return False
        return True

    def __hash__(self):
        return hash(str(self))

    def __add__(self, other):
        """Defines addition of two nichols elements with the '+' syntax in python.

        Inputs must be elements from the class. Returns another nichols element.
        Essentially, what it does is the concatenation of the dictionaries and adds the coefficients for the same
        monomial term.
        """
        newdic = self.poly.copy()
        for term, sca in other.pairs:
            if term in newdic:
                newdic[term] += sca
            else:
                newdic[term] = sca
        return type(self)(newdic).rewrite()

    def __sub__(self, other):
        """Defines subtraction of two nichols elements with the '-' syntax in python.
        """
        return self + type(self)({"": -1})*other

    def __mul__(self, other):
        """Defines multiplication of two nichols elements.

        As for classical polynomials, it consists of the linear expansion of the terms and concatenation pairwise of
        monomial terms (and product of the respetive coefficients).
        """
        newpoly = type(self)({})
        for term1, sca1 in self.pairs:
            for term2, sca2 in other.pairs:
                newterm = term1 + term2
                newpoly += type(self)({newterm: sca1*sca2})
        return newpoly.rewrite()

    def __delitem__(self, term):
        """Auxiliary method."""
        del self.poly[term]

    def rewrite(self):
        """Simply remove elements with scalar zero.
        """
        newpoly = Element(self.poly.copy())  # Create a copy to begin with.
        for term, sca in newpoly.pairs:
            # Run through the monomial terms recursively, applying the relations whenever possible. Bergman's Diamond
            # lemma guarantees this works.
            if sca == 0:
                # Monomial terms with corresponding coefficient 0 are deleted.
                del newpoly[term]
                return newpoly.rewrite()
        return newpoly

    def coproduct(self):
        """ 
            Returns the coproduct of an element by using the linearity of the coproduct
            I.e. cop(ab+ 3cd) = cop(ab)+ 3* cop(cd)
            
            The function splits each element into its words, 
            calls the coproduct function on each word,
            multiplies the result with the associated coefficient
            and returns the sum of all these tensor elements
        """
        return sum([term.coproduct().scalar_mulitply(sca) for term, sca in self.pairs], 
                   tensor_element.TensorElement({word.TensorWord(
                       [word.Word([]), word.Word([])]):0}))
        
    def c_bilinear(self, other):
        """
            Computes the value of the c bilinear form of an element wrt to another element.
            It uses the bilineary to  compute say (ab+4xy, cd+ 2z) as
            (ab,cd)+ 2*(ab,z) +4(xy,cd)+ 8(xy,z)
            
            The function splits the element self and other into each word.
            For every such pair of words it computs the c-bilnear on this pair,
            multiplies it with the respective coefficients
            and sums everything up.
        """                
        output_number = 0
        
        for term_1,sca_1 in self.pairs:
            for term_2, sca_2 in other.pairs:
                output_number += sca_1*sca_2* term_1.c_bilinear(term_2)
    
        return output_number

    @classmethod
    def set_universe(cls, a) -> None:
        Element.universe = a
        Element.generators = a.generators
        Element.base_field = a.base_field
        Element.variables = a.variables
        Element.q_matrix = a.q_matrix


def create_element(string, scalar=1):
    """The most pratical way to construct a new element. Constructs individual monomials (with an optional scalar).
    Inputs: string, scalar (one by default).
    Output: element of the form 'scalar times string' written in the PBW basis.
    """
    if string == 0:
        newelement = Element({'': 0})
    else:
        newelement = Element({string: scalar})
    return newelement.rewrite()


def present(input):
    """Auxiliary function for processing the string of a monomial.

     Takes a string with concatenation of repeated letters and returns the string with exponents and
     parenthesis, to improve readibility.

    Input: string
    Output: string
    Example: present('aaa') outputs 'a^3'
    """
    string = str(input)
    if len(string) <= 1:
        return string
    word = ''
    i = 0
    while i < len(string):
        # for different letters
        k = 1
        while i < len(string):
            # to count a letter
            if i == len(string) - 1:
                i += 1
                break
            elif string[i + 1] == string[i]:
                k += 1
                i += 1
            else:
                i += 1
                break
        if k == 1:
            word += string[i - 1]
        elif string[i - 1] == ")":
            word += "))"
        else:
            word += string[i - 1] + "^" + str(k)
    return word

def q_bilinear(first: Element, second: Element):
    """Computes the q-bilinear form between two PBW generators."""
    # TODO

    return


def bracket(first: Element, second: Element) -> Element:
    """ Computes the q-commutator bracket [first, second]_q."""
    # TODO verify

    return first*second - create_element('', q_bilinear(first, second))*second*first
