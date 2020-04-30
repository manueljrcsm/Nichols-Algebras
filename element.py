# -*- coding: utf-8 -*-

import tensor_element as te
import universe as u
import word as w


class Element:
    """Elements in the free algebra live here.
    """
    
    __slots__ = ("poly", "scalars", "terms", "pairs")

    def __init__(self, dic):
        """An object's structure is stored in a dictionary. Defines some attributes of the element which can
            then be manipulated.
        """
        object.__setattr__(self, "poly", dic.copy())
        object.__setattr__(self, "scalars", dic.values())
        object.__setattr__(self, "terms", dic.keys())
        object.__setattr__(self, "pairs", dic.items())
        
    def __setattr__(self, name: str, value):
        
        msg = "It is not allowed to change the value of the attribute '" + name + "'."
        raise AttributeError(msg)

    def __str__(self):
        """Creates the string representation of an element, i.e., what you see when you do '
        (element)'.
        """
        word = ""

        for term, sca in self.pairs:
            # Run through the monomial terms of the element.z
            scalar = str(sca)
            sign = " + "
            if scalar[0]== "-":
                    sign = " - "
                    scalar = str(-1*sca)
            if scalar == "1" and str(term) != "":
                # If the coefficient of a term is 1, then it is ommited.
                scalar = ""
            elif "+" or " - " in scalar:
                scalar = "(" + scalar + ")"
            
            word += sign + scalar + str(term)
            
        if word == "":  # Empty dictionaries correspond to the 0 element.
            return "0"
        else:
            return word[3:]

    def __eq__(self, other):
        """Defines when two elements are equal.

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
        """Defines addition of two elements with the '+' syntax in python.

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
        """Defines subtraction of two elements with the '-' syntax in python.
        """
        return self + type(self)({w.Word([]): -1})*other

    def __mul__(self, other):
        """Defines multiplication of two elements.

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

    def scalar_multiply(self, number):
        """Scales an element by the given number."""

        if number == 0:
            return u.Universe.ElementZERO
        # TODO CHECK THAT NUMBER IS INT FLOAT SAGE_SCALAR
        if number == 1:
            return Element(self.poly.copy())
        output_dict = {}
        for term, scalar in self.pairs:
            output_dict[term] = scalar*number
        return Element(output_dict)

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
                   te.TensorElement({w.TensorWord(
                       [w.Word([]), w.Word([])]):0}))

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


    # TODO delete this
    # def q_bilinear(self, other):
    #     """ Computes the q-bilinear form between two elements. This function splits the form linearly into pairs of
    #     words and calls the corresponding method from the class Word.
    #     """
    #     output_number = 0
    #
    #     for term_1, sca_1 in self.pairs:
    #         for term_2, sca_2 in other.pairs:
    #             output_number += sca_1*sca_2*term_1.q_bilinear(term_2)
    #
    #     return output_number
