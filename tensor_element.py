# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 20:00:44 2020

@author: manue
"""
from element import Element


class TensorElement:
    """Its objects are a formal sum of pure tensors in A^{\otimes 2}  with scalar coefficients,
    pure tensors are a pair (tuple) of objects of the class element (NOT simply strings).
    """

    def __init__(self, dic):
        newdic = {}
        if dic != {}:
            for pair, sca in dic.items():  # Pair is a tuple, sca is a number.
                newfirst = pair[0].rewrite()  # In case the input is not in standard form.
                newsecond = pair[1].rewrite()  # Idem.
                for term1, sca1 in newfirst.pairs:  # Here term1 is string, sca1 is number.
                    for term2, sca2 in newsecond.pairs:  # Idem.
                        newsca = sca1*sca2*sca  # Each tensorand may have its own scalar, so when you expand
                        # everything, you want to combine these scalars.
                        newpair = Element({term1: 1}), Element(
                            {term2: 1})  # The new tuple is generated  without scalars, which go into the global scalar.
                        newdic[newpair] = newsca

        # Attributes
        self.dic = newdic
        self.tensors = newdic.keys()
        self.scalars = newdic.values()
        self.items = newdic.items()


def __str__(self):
    word = ""
    i = 0
    for pair, sca in self.items:
        scalar = str(sca)
        first = str(pair[0])
        second = str(pair[1])
        if scalar == "1":
            scalar = ""
        if first == "":
            first = "1"
        if second == "":
            second = "1"
        if i > 0:
            if scalar[0:1] == '-':
                word += " - "
                if scalar == "-1":
                    scalar = ""
                else:
                    scalar = str(sca)[1:]
            else:
                word += " + "
        if len(scalar) > 3:
            scalar = "(" + scalar + ")"
        word += scalar + "(" + first + u"\u2297" + second + ")"  # u"\u2297" is the \otimes symbol.
        i += 1
    if word == "":
        return "0"
    else:
        return word


def __add__(self, other):
    newdic = self.dic.copy()
    for pair, sca in other.items:
        if pair in newdic:
            newdic[pair] += sca
        else:
            newdic[pair] = sca
    newtensor = TensorElement(newdic)
    return newtensor.rewrite()


def __mul__(self, other):
    zero = Element({"": 0})
    newtensor = tensorize(zero, zero)  # Check definition of tensorize, simpler constructor.
    for pair1, sca1 in self.items:
        for pair2, sca2 in other.items:
            newpair = (pair1[0]*pair2[0], pair1[1]*pair2[1])  # Braiding would come into play here.
            newsca = sca1*sca2
            newtensor += TensorElement({newpair: newsca})
    return newtensor.red()


def __delitem__(self, term):
    del self.dic[term]


def copy(self):
    return TensorElement(self.dic)


def rewrite(self):
    """Cleaning zero terms."""
    newtensor = self.copy()
    for pair, sca in newtensor.items:
        if sca == 0:
            del newtensor[pair]
    return newtensor


def tensorize(first, second, sca=1):
    """Takes two algebra elements, returns the corresponding pure tensor. """
    newdic = {(first, second): sca}
    return TensorElement(newdic)
