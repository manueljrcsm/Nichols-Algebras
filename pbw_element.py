# -*- coding: utf-8 -*-
from element import element

try:
    from sage.all_cmdline import *  # imports sage library

    _sage_const_2 = Integer(2);
    _sage_const_1 = Integer(1)
    names = ('p', 'q', 'r')  # tuple of strings with the q matrix
    P = FractionField(PolynomialRing(QQ, 3, 'p,q,r'))
# K = NumberField(u**_sage_const_2  + u + _sage_const_1 , names=('q',)); (q,) = K._first_ngens(1) #K is the field containing a primitive third root of unity 'r'

## OPTIONAL: This code is to create variables in the field, that can be used as placeholders in generic linear combinations. Computation can be made to then derive relations or conditions and find out
## precisely what the linear combination coefficients must be.
# A = PolynomialRing(K, 3,names=('alpha','beta','gamma',)) #to find linear combination of elements
# (alpha, beta, gamma,) = A._first_ngens(3)
except:  # IGNORE
    q = 2
    p = 3
    r = 5
    print("Sage Module not found, (p,q,r)=(%s,%s,%s)"%(p, q, r))

RELATIONS = {}


class pbw_element(element):
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
            To change this to writing the monomials with the order z > y >x > v > u >t, you would change it here.
        """
        # Relations are added here, this can be moved elsewhere or passed as an argument
        RELATIONS['zt'] = pbw_element({'tz': q, 'u': 1})
        RELATIONS['zu'] = pbw_element({'uz': p * q, 'x': 1})
        RELATIONS['zx'] = pbw_element({'xz': p * p * q, 'y': 1})
        RELATIONS['xu'] = pbw_element({'ux': p * p * q * q * q * r, 'v': 1})
        RELATIONS['zy'] = pbw_element({'yz': p * p * p * q})
        RELATIONS['ut'] = pbw_element(
            {'tu': (1 + r - r * q * q) / (q * r), 'ttz': (1 - q * q) * (1 - q * q * r) / (q * q * r)})

        newpoly = pbw_element(self.poly.copy())  # create a copy to begin
        for term, sca in newpoly.pairs:
            # run through the monomial terms recursively, applying the relations whenever possible. Bergman's Diamond
            # lemma guarantees this works.
            if sca == 0:
                # monomial terms with corresponding coefficient 0 are deleted
                del newpoly[term]
                return newpoly.rewrite()
            for i in range(len(term) - 1):
                if term[i] + term[i + 1] in RELATIONS.keys():
                    # TODO: This presupposes that the relations are skew-commutations
                    del newpoly[term]
                    newpoly += pbw_element({term[:i]: sca}) * RELATIONS[term[i] + term[i + 1]] * pbw_element(
                        {term[i + 2:]: 1})
                    return newpoly.rewrite()
        return newpoly


def create_pbw_element(string, scalar=1):
    """The most pratical way to construct a new element. Constructs individual monomials (with an optional scalar).
    Inputs: string, scalar (one by default).
    Output: pbw_element of the form 'scalar times string' written in the PBW basis.
    """
    if string == 0:
        newelement = pbw_element({'': 0})
    else:
        newelement = pbw_element({string: scalar})
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

