# -*- coding: utf-8 -*-
from element import Element
import pbw_algebra

class PBWElement(Element):
    """Class whose objects are elements in the Nichols algebra B.

    Elements are polynomials with coefficients in P. These elements are represented by Python dictionaries.
    The keys in the dictionary are strings, corresponding to monomials on the in the PBW generators. The value of a
    given key is the coefficient that comes with that monomial term. The commutation relations are given by the
    global list RELATIONS.

    Functionalities: print, comparison (equality test), addition, subtraction, multiplication, reduction to the basis
    (with order a < xa < x)

    Inherits the methods __str__, __add__,__sub__, __mul__, __eq__, __delitem__ and __hash__ from 'element'.
    Overrides the method rewrite().
    """

    # TODO needs scalar multiplication,  ordered presentation, lookup terms of certain form (lexicographic order on
    #  the monomials), presentation of exponentials,

    # Class attributes
    pbw_universe = None
    relations = {}

    def rewrite(self):
        """Reduction of a polynomial to its standard basis form t > u > v > x > y > z. Where it really gets
        interesting and where the commutation relations are applied.
        The relations are
            zt = qtz + u
            zu = (pq)uz + x
            zx = (p^2q)xz + y
            xu = (p^2q^3r)ux + v
            zy = (p^3q)yz
            ut = (1+ r - rq^2)/(qr) tu - (1-q^2)(1 - q^2r)/(q^2r) t^2z
        """
        # Relations are added here, this can be moved elsewhere or passed as an argument
        newpoly = PBWElement(self.poly.copy())  # create a copy to begin
        relations = PBWElement.relations
        for term, sca in newpoly.pairs:
            # Run through the monomial terms recursively, applying the relations whenever possible. Bergman's Diamond
            # lemma guarantees this works.
            if sca == 0:
                # Monomial terms with corresponding coefficient 0 are deleted
                del newpoly[term]
                return newpoly.rewrite()
            for i in range(len(term) - 1):
                if term[i] + term[i + 1] in relations.keys():
                    # TODO: This presupposes that the relations are skew-commutations
                    del newpoly[term]
                    newpoly += PBWElement({term[:i]: sca})*relations[term[i] + term[i + 1]]*PBWElement(
                        {term[i + 2:]: 1})
                    return newpoly.rewrite()
        return newpoly

    def c_norm(self):
        """Computes (self|self) in terms of the norms of the PBW generators."""
        # TODO
        return

    def isHomogenous(self) -> bool:
        """Checks if a polynomial is homogenous."""
        # TODO

        return

    @classmethod
    def set_universe(cls, a) -> None:
        PBWElement.universe = a
        PBWElement.generators = a.generators
        PBWElement.base_field = a.base_field
        PBWElement.variables = a.variables
        PBWElement.q_matrix = a.q_matrix
        PBWElement.relations = a.relations

def create_pbw_element(string, scalar=1):
    """The most pratical way to construct a new element. Constructs individual monomials (with an optional scalar).

    Inputs: string, scalar (one by default).
    Output: pbw_element of the form 'scalar times string' written in the PBW basis.
    """
    if string == 0:
        newelement = PBWElement({'': 0})
    else:
        newelement = PBWElement({string: scalar})
    return newelement.rewrite()


def show_element(newelement):
    """Enumerates the terms of a nichols class element. Use it as a better form of 'print', for very long elements.

    Input: nichols class element
    Output: one monomial term per line
    """
    i = 1
    for term, sca in newelement.pairs:
        print(str(i) + " (" + str(create_pbw_element(term)) + ") : " + str(sca))
        i += 1
    print("END")
