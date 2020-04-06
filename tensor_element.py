# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 20:00:44 2020

@author: manue
"""
# from element import Element
from word import Word
import copy


class TensorElement:
    """Its objects are a formal sum of pure tensors in A^{\otimes 2}  with scalar coefficients,
    pure tensors are a pair (tuple) of objects of the class element (NOT simply strings).
    """

    __slots__ = ("dic", "tensor_terms", "scalars", "pairs")

    def __init__(self, dic: dict):

        if all(type(e) is tuple and all(type(f) is Word for f in e) for e in list(dic.keys())):

            new_dic = {}
            for tensorand, scalar in dic.items():
                if not scalar == 0:
                    new_dic[tensorand] = scalar
            object.__setattr__(self, "dic", new_dic)
            object.__setattr__(self, "tensor_terms", new_dic.keys())
            object.__setattr__(self, "scalars", new_dic.values())
            object.__setattr__(self, "pairs", new_dic.items())


        else:
            msg = "The tensor element was not in the expected format"
            raise AssertionError(msg)
        """
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
        """

    def __str__(self):
        word = ""
        for tensor_term, sca in self.pairs:
            scalar = str(abs(sca)) if (sca != 1) else ""
            word = word + " + " if (sca > 0) else word + " - "
            word += scalar + (u'\u2297').join(str(w) for w in tensor_term)
        if len(word) == 0:
            return ""
        elif word[0:3] == " + ":
            return word[3:]
        else:
            return word

    def __setattr__(self, name: str, value):

        msg = "It is not allowed to change the value of the attribute '" + name + "'."
        raise AttributeError(msg)

    def __add__(self, other):

        print("I'm requested to add ", self, " and ", other)
        output_dict = other.dic.copy()
        for tensor_term, sca in self.pairs:
            if tensor_term in other.dic:
                if sca + output_dict[tensor_term] == 0:
                    output_dict.pop(tensor_term)
                else:
                    output_dict[tensor_term] += sca
            else:
                output_dict[tensor_term] = sca

        return TensorElement(output_dict)

    def __sub__(self, other):
        return self + other.scalar_mulitply(-1)

    def __mul__(self, other):
        output_dict = {}
        if not all(len(e) == len(list(self.tensor_terms)[0]) for e, f in self.pairs):
            msg = "You tried to muliply tensorands of different length. This is not supported."
            raise AssertionError(msg)
        for tensor_term_1, sca_1 in self.pairs:
            for tensor_term_2, sca_2 in other.pairs:
                if (len(tensor_term_1) != len(tensor_term_2)):
                    msg = "You tried to muliply tensorands of different length. This is not supported."
                    raise AssertionError(msg)
                else:
                    word_list = []
                    for i in range(len(tensor_term_1)):
                        word_list.append(tensor_term_1[i] + tensor_term_2[i])

                    if not tuple(word_list) in output_dict:
                        output_dict[tuple(word_list)] = sca_1*sca_2
                    else:
                        output_dict[tuple(word_list)] += sca_1*sca_2
        return TensorElement(output_dict)

    def scalar_mulitply(self, number):

        print("The term", self, "should be scalary muliplied by ", number)

        if (number == 0):
            return TensorElement({})
        # TODO CHECK THAT NUMBER IS INT FLOAT SAGE_SCALAR
        if (number == 1):
            return self
        output_dict = {}
        for tensor_term, scalar in self.pairs:
            output_dict[tensor_term] = scalar*number
        result = TensorElement(output_dict)
        print(result)
        return result

    def __delitem__(self, term):
        del self.dic[term]

    def copy(self):
        return TensorElement(self.dic)

    def rewrite(self):
        """Cleaning zero terms."""
        newtensor = self.copy()
        for pair, sca in newtensor.pairs:
            if sca == 0:
                del newtensor[pair]
        return newtensor

    def tensorize(first, second, sca=1):
        """Takes two algebra elements, returns the corresponding pure tensor. """
        newdic = {(first, second): sca}
        return TensorElement(newdic)
